from django.shortcuts import render
from django.contrib.auth.models import User
from models import UserAccount

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import constants
import helpers
import models

import os
import simplejson as json
from PIL import Image


class GenericView(object):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request")
        if not self.request:
            # TODO raise proper exception
            raise("No request passed to view")

        self._sourcePage = kwargs.get("sourcePage")
        self._currentPage = kwargs.get("currentPage")
        self._currentPageHtml = None
        self._currentPageURL = None
        self._destinationPage = None
        self._destPageKey = None

        self._userAccount = None
        self._username = None
        self._pageErrors = []  #TODO
        self._cancelButtonExtraInputs = {}
        self._cancelDestination = None
        self._cancelDestinationURL = None
        self._cancelSource = None
        self._cancelButtonName = "Cancel"

        self.errorMemory = {}

        # Need to setup the base context first so child classes can add to it
        self._pageContext = {}
        self.setupBaseContext()

    def setupBaseContext(self):
        if not self._pageContext:
            self._pageContext = helpers.getBaseContext(self.request)
        self._pageContext["source"] = self.sourcePage
        self._pageContext["next"] = self.currentPage
        self._pageContext["destination"] = self.destinationPage
        self._pageContext["currentPageURL"] = self.currentPageURL
        self._pageContext["cancelButtonExtraInputs"] = json.dumps(self.cancelButtonExtraInputs)
        self._pageContext["cancelDestinationURL"] = self.cancelDestinationURL
        self._pageContext["cancelDestination"] = self.destinationPage
        self._pageContext["cancelButtonName"] = self.cancelButtonName
        self._pageContext["cancelSource"] = self.cancelSource
        self._pageContext["cancelDestination"] = self.cancelDestination

    @property
    def cancelSource(self):
        if self._cancelSource is None:
            self._cancelSource = self.sourcePage
        return self._cancelSource

    @property
    def cancelDestination(self):
        if self._cancelDestination is None:
            if self.sourcePage in [constants.HOME, constants.LOGIN, constants.SETUP_ACCOUNT_FINISH,
                                   constants.CREATE_BASIC_ACCOUNT_FINISH]:
                self._cancelDestination = constants.HOME
            else:
                self._cancelDestination = self.request.POST.get("cancelDestination") or self.sourcePage
        return self._cancelDestination

    @property
    def cancelDestinationURL(self):
        if self._cancelDestinationURL is None:
            self._cancelDestinationURL = constants.URL_MAP.get(self.currentPage)
        return self._cancelDestinationURL

    @property
    def cancelButtonExtraInputs(self):
        return self._cancelButtonExtraInputs or {}

    @property
    def cancelButtonName(self):
        return self._cancelButtonName

    @property
    def pageContext(self):
        """To be overridden in child class"""
        self._pageContext["errors"] = self.pageErrors
        self._pageContext["cancelButtonExtraInputs"] = self.cancelButtonExtraInputs
        return self._pageContext

    @property
    def pageErrors(self):
        "TODO"
        return self.errorMemory

    @property
    def sourcePage(self):
        if self._sourcePage is None:
            if self.request.POST.get("source"):
                self._sourcePage = self.request.POST.get("source")
            else:
                self._sourcePage = helpers.getMessageFromKey(self.request, "source")
                if not self._sourcePage:
                    self._sourcePage = constants.HOME
        return self._sourcePage

    @property
    def currentPage(self):
        if self._currentPage is None:
            if self.request.POST.get("next"):
                self._currentPage = self.request.POST.get("next")
            else:
                self._currentPage = self.sourcePage
        return self._currentPage

    @property
    def currentPageHtml(self):
        if self._currentPageHtml is None:
            self._currentPageHtml = constants.HTML_MAP.get(self.currentPage)
        return self._currentPageHtml

    @property
    def currentPageURL(self):
        if self._currentPageURL is None:
            self._currentPageURL = constants.URL_MAP.get(self.currentPage)
        return self._currentPageURL

    @property
    def destinationPage(self):
        if self._destinationPage is None:
            if self.request.POST.get("destination"):
                self._destinationPage = self.request.POST.get("destination")
            elif helpers.getMessageFromKey(self.request, "destination"):
                self._destinationPage = helpers.getMessageFromKey(self.request, "destination")
            if self._destinationPage in [None, constants.DEFAULT]:
                self._destinationPage = constants.DEFAULT_PAGE_MAP.get(self.currentPage)
        return self._destinationPage

    @property
    def destPageKey(self):
        """Used when multiple destination options for same source and current page combo"""
        return self._destPageKey

    @property
    def userAccount(self):
        if self._userAccount is None:
            self._userAccount = UserAccount.objects.get(username=self.username)
        return self._userAccount

    @property
    def username(self):
        if self._username is None:
            self._username = self.request.user.username
        return self._username

    def process(self):
        if self.request.method == "POST" and self.checkFormValidity():
            return helpers.redirect(request=self.request,
                                    currentPage=self.currentPage,
                                    destinationPage=self.destinationPage)

        # Need to access pageContext before setting variables
        # !!!!!!!!!! Don't delete
        self.pageContext
        # !!!!!!!!!!
        if self.pageErrors:
            self._pageContext["errors"] = self.pageErrors
        print "source :{0}, current: {1}, dest: {2}".format(self.sourcePage, self.currentPage, self.destinationPage)
        return render(self.request, self.currentPageHtml, self.pageContext)



class GenericFormView(GenericView):
    def __init__(self, *args, **kwargs):
        super(GenericFormView, self).__init__(*args, **kwargs)
        self._form = None
        self._formClass = None
        self._formInitialValues = {}
        self._formSubmitted = None
        self._formData = None
        self.setupFormInitialValues()

    def setupFormInitialValues(self):
        self._formInitialValues["source"] = self.currentPage
        self._formInitialValues["next"] = self.currentPage
        self._formInitialValues["destination"] = self.destinationPage
        self._formInitialValues["cancelDestination"] = self.cancelDestination

    @property
    def formClass(self):
        if not self._formClass:
            self._formClass = constants.FORM_MAP.get(self.currentPage)
        return self._formClass

    @property
    def formSubmitted(self):
        self._formSubmitted = self.currentPage == self.sourcePage
        return self._formSubmitted

    @property
    def formInitialValues(self):
        # To override in child class
        return self._formInitialValues

    @property
    def formData(self):
        if self._formData is None:
            if self.formClass is None:
                self._formData = self.request.POST
            else:
                self._formData = self.form.is_valid() and self.form.cleaned_data
        return self._formData

    @property
    def form(self):
        if not self._form:
            if self.formSubmitted and self.formClass:
                self._form = self.formClass(self.request.POST)
            elif self.formClass:
                self._form = self.formClass(initial=self.formInitialValues)
        return self._form

    def checkFormValidity(self):
        formIsValid = False
        if self.request.POST.get(constants.CANCEL) != "True":
            if self.formSubmitted:
                if self.formClass:
                    if self.form.is_valid():
                        self.errorMemory = self.formData
                        formIsValid = self.processForm()
                    else:
                        self.errorMemory = self.request.POST
                else:
                    formIsValid = self.processForm()
        else:
            self.cancelPage()
            formIsValid = True
        return formIsValid

    def cancelPage(self):
        self._destinationPage = self.cancelDestination
        self._pageContext["destination"] = self.cancelDestination

    def process(self):
        if self.request.method == "POST" and self.checkFormValidity():
            return helpers.redirect(request=self.request,
                                    currentPage=self.currentPage,
                                    destinationPage=self.destinationPage)

        # Need to access pageContext before setting variables
        # !!!!!!!!!! Don't delete
        self.pageContext
        self.formInitialValues
        # !!!!!!!!!!
        self._pageContext["form"] = self.form
        if self.pageErrors:
            self._pageContext["errors"] = self.pageErrors
        print "source :{0}, current: {1}, dest: {2}".format(self.sourcePage, self.currentPage, self.destinationPage)
        return render(self.request, self.currentPageHtml, self.pageContext)

    def processForm(self):
        """To bo overridden in child class"""
        return True


class PictureFormView(GenericFormView):
    def __init__(self, *args, **kwargs):
        super(PictureFormView, self).__init__(*args, **kwargs)
        self._pictureModel = None
        self._pictureModelPictureField = None
        self._pictureModelFieldName = None
        self._cropInfo = {}
        self._filename = None
        self._sourcePicture = None


    @property
    def sourcePicture(self):
        if self._sourcePicture is None:
            self._sourcePicture = self.request.FILES.get(self.pictureModelFieldName)
        return self._sourcePicture

    @property
    def filename(self):
        if self._filename is None:
            self._filename = MEDIA_FILE_NAME_MAP.get(self.request.POST.get("source"), "tempfile")
        return self._filename

    @property
    def form(self):
        """To be overridden in child class"""
        if not self._form:
            if self.formSubmitted:
                # Override form to create form with request.FILES
                self._form = self.formClass(self.request.POST, self.request.FILES)
            elif self.formClass:
                self._form = self.formClass(initial=self.formInitialValues)
        return self._form

    @property
    def pictureModel(self):
        # like event
        return self._pictureModel

    @property
    def pictureModelPictureField(self):
        # like event.eventPicture
        # Need to return updated field each time is accessed (since the field is set independently)
        self._pictureModelPictureField = self.pictureModel.__dict__[self.pictureModelFieldName]
        return self._pictureModelPictureField

    @property
    def pictureModelFieldName(self):
        # Like eventPicture
        return self._pictureModelFieldName

    def checkFormValidity(self):
        formIsValid = False
        if "True" not in [self.request.POST.get(constants.CANCEL),
                          self.request.POST.get("redirect")]:
            if self.formSubmitted:
                if self.formClass:
                    if self.form.is_valid():
                        self.errorMemory = self.formData
                        if self.processForm():
                            if self.updatePicturePathAndModel():
                                formIsValid = True
                            else:
                                print "Failure saving form image"
                        else:
                            print "Failure processing form"
                    else:
                        print "Form errors: {0}".format(self.form.errors)
                        self.errorMemory = self.form.errors
                else:
                    print "No form class"
                    if self.processForm():
                        formIsValid = True
            else:
                print "Form not submitted"
        else:
            print "Not processing form because cancel or redirect is True"
            self.cancelPage()
            formIsValid = True
        if not formIsValid:
            print "Failure checking form validity: {0}".format(self.errorMemory)
        return formIsValid

    @property
    def cropInfo(self):
        if not self._cropInfo:
            self._cropInfo = {"x": self.request.POST.get("crop_x"),
                              "y": self.request.POST.get("crop_y"),
                              "width": self.request.POST.get("crop_width"),
                              "height": self.request.POST.get("crop_height")}

            # Need all 4 values to crop, so if missing any, don't perform the crop
            if None in self._cropInfo.values():
                self._cropInfo = {}
        return self._cropInfo

    def updatePicturePathAndModel(self):
        if self.pictureModel:
            # No file but cropInfo means crop existing pic
            # No cropInfo and no file means save None
            if self.sourcePicture or (not self.sourcePicture and not self.cropInfo):
                # Save the InMemoryUploadedFile instance in the file field of the model
                self._pictureModelPictureField = self.sourcePicture
                self.pictureModel.save()

                # Fall back if source picture does not come from request
                if not self.pictureModelPictureField:
                    self.pictureModel.__dict__[self.pictureModelFieldName] = self.sourcePicture

            if self.pictureModelPictureField:
                if self.cropInfo:
                    image = Image.open(self.pictureModelPictureField.path)
                    x = float(self.cropInfo.get("x"))
                    y = float(self.cropInfo.get("y"))
                    croppedImage = image.crop((x, y, float(self.cropInfo["width"]) + x, float(self.cropInfo["height"]) + y))
                    croppedImage.save(self.pictureModelPictureField.path)
                    croppedImage = croppedImage.resize((810, 900), Image.ANTIALIAS)
                    croppedImage.save(self.pictureModelPictureField.path)

                # Rename picture file
                newPath = os.path.join(os.path.dirname(self.pictureModelPictureField.path), self.filename)
                os.rename(self.pictureModelPictureField.path, newPath)
                self._pictureModelPictureField.name = os.path.join(self.request.user.username, self.filename)
                self.pictureModel.save()
                return True
            elif not self.sourcePicture:
                # Should still be a success when no picture is added
                return True
        return False