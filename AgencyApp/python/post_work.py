import post
import constants
import models
import helpers

import json

class WorkPostInstance(post.GenericPostInstance):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.WORK_POST
        self._projectID = kwargs.get("projectID")
        super(WorkPostInstance, self).__init__(*args, **kwargs)
        self._database = models.WorkPost

    def checkModelFormValues(self):
        valid = False
        if self.request.method == "POST":
            if len(self.request.POST.get("profession", "")) < 1:
                self.errors.append("Missing profession")
            else:
                valid = True
        return valid

    def saveModelFormValues(self):
        if self.record:
            self.record.profession = self.request.POST.get("profession")
            self.record.projectID = self.request.POST.get("projectID")
            self.record.compensationType = self.request.POST.get("compensationType")
            self.record.compensationDescription = self.request.POST.get("compensationDescription")
            self.record.shortDescription = self.request.POST.get("shortDescription")
            self.record.workerName = self.request.POST.get("workerName")
            self.record.skills = self.request.POST.get("skills")
            self.record.hoursPerWeek = self.request.POST.get("hoursPerWeek")
            self.record.startDate = self.request.POST.get("startDate")
            self.record.endDate = self.request.POST.get("endDate")
            self.record.location = self.request.POST.get("location")
            self.record.workerNeedsEquipment = self.request.POST.get("workerNeedsEquipment", False) and True
            self.record.equipmentDescription = self.request.POST.get("equipmentDescription")
            self.record.save()
            return True
        return False


class CreateWorkPostView(post.GenericCreatePostView):
    def __init__(self, *args, **kwargs):
        kwargs["postType"] = constants.WORK_POST
        super(CreateWorkPostView, self).__init__(*args, **kwargs)
        self._worker = None

    @property
    def worker(self):
        if self._worker is None:
            if self.post and self.post.record and self.post.record.status == "Filled":
                try:
                    self._worker = models.UserAccount.objects.get(username=self.post.record.workerName)
                except models.UserAccount.DoesNotExist:
                    pass
        return self._worker

    @property
    def post(self):
        if self._post is None:
            self._post = WorkPostInstance(request=self.request, postID=self.postID, projectID=self.projectID,
                                          postType=constants.WORK_POST, formSubmitted=self.formSubmitted)
        return self._post

    @property
    def pageContext(self):
        self._pageContext = super(CreateWorkPostView, self).pageContext
        self._pageContext["professionList"] = json.dumps(constants.PROFESSIONS)
        self._pageContext["defaultStatus"] = "Open"
        self._pageContext["worker"] = self.worker
        self._pageContext["isWork"] = True
        return self._pageContext

    @property
    def formInitialValues(self):
        self._formInitialValues = super(CreateWorkPostView, self).formInitialValues
        if self.post.record:
            self._formInitialValues["compensationType"] = self.post.record.compensationType
            self._formInitialValues["compensationDescription"] = self.post.record.compensationDescription
            self._formInitialValues["skills"] = self.post.record.skills
            self._formInitialValues["hoursPerWeek"] = self.post.record.hoursPerWeek
            self._formInitialValues["startDate"] = self.post.record.startDate
            self._formInitialValues["endDate"] = self.post.record.endDate
            self._formInitialValues["shortDescription"] = self.post.record.shortDescription
            if self.worker:
                self._formInitialValues["workerName"] = self.worker.username
            self._formInitialValues["postID"] = self.post.record.postID
            self._formInitialValues["projectID"] = self.post.projectID
            self._formInitialValues["profession"] = self.post.record.profession
            self._formInitialValues["location"] = self.post.record.location
            self._formInitialValues["workerNeedsEquipment"] = self.post.record.workerNeedsEquipment
            self._formInitialValues["equipmentDescription"] = self.post.record.equipmentDescription
        return self._formInitialValues


class ViewWorkPostView(post.GenericViewPostView):
    def __init__(self, *args, **kwargs):
        super(ViewWorkPostView, self).__init__(*args, **kwargs)
        self._job = None
        self._worker = None

    @property
    def pageContext(self):
        self._pageContext = super(ViewWorkPostView, self).pageContext
        self._pageContext["possibleDestinations"] = {"editPost": constants.EDIT_POST,
                                                     "viewPost": constants.VIEW_POST}
        self._pageContext["job"] = self.job
        self._pageContext["worker"] = self.worker
        self._pageContext["isWork"] = True
        return self._pageContext


    @property
    def job(self):
        if self._job is None:
            try:
                self._job = models.WorkPost.objects.get(postID=self.postID)
            except models.ProjectWorkPost.DoesNotExist:
                pass
        return self._job

    @property
    def worker(self):
        if self._worker is None:
            if self.post.record.status == "Filled" and self.job:
                try:
                    self._worker = models.UserAccount.objects.get(username=self.job.workerName)
                except models.UserAccount.DoesNotExist:
                    pass
        return self._worker

    @property
    def post(self):
        if self._post is None:
            if self.postID:
                self._post = WorkPostInstance(request=self.request, postID=self.postID, postType=constants.WORK_POST)
        return self._post

    @property
    def postTitle(self):
        if self._postTitle is None:
            if self.post and self.post.record:
                self._postTitle = self.post.record.profession + " Wanted"
        return self._postTitle

    @property
    def postSubTitles(self):
        if not self._postSubTitles:
            if self.post and self.post.record:
                self._postSubTitles = [self.post.record.title]
        return self._postSubTitles

    @property
    def postFieldsBySection(self):
        if not self._postFieldsBySection:
            if self.post and self.post.record:
                self._postFieldsBySection = {"Details": [{'id': 'status', 'value': self.post.record.status, 'label': 'Status'},
                                                        {'id': 'dates', 'value': helpers.getDateString(self.post.record.startDate, self.post.record.endDate), 'label': None},
                                                        {'id': 'location', 'value': self.post.record.location, 'label': 'Location'},
                                                        {'id': 'compensation', 'value': self.post.record.compensation, 'label': 'Compensation'},
                                                        {'id': 'hoursPerWeek', 'value': self.post.record.hoursPerWeek, 'label': 'Hours/Week'},
                                                        ]}
                """Position": [{'id': 'gender', 'value': self.post.record.gender, 'label': 'Gender'},
                                                          {'id': 'ageRange', 'value': self.post.record.ageRange, 'label': 'Age Range'},
                                                          {'id': 'characterType', 'value': self.post.record.characterType, 'label': 'Type'}
                                                         ],
                                            "Description": [{'id': 'description', 'value': self.post.record.description, 'label': None}
                                                            ]
                                            }"""
                
                # Add project to front of list if it is linked
                if self.project and self.project.record:
                    self._postFieldsBySection["Details"] = [{'id': 'project', 'value': self.project.record.title, 'label': 'Project',
                                                             'onclick': 'redirectToPost("{0}");'.format(self.project.record.postID)}] + self._postFieldsBySection["Details"]
        return self._postFieldsBySection


