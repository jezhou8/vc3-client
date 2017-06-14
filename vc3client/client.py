#!/bin/env python
__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

import ast
import json
import logging
import os
import yaml

from entities import User, Project, Resource, Allocation, Request, Cluster, Environment
from vc3infoservice import infoclient

class VC3ClientAPI(object):
    '''
    Client application programming interface. 
    
    -- DefineX() methods return object. CreateX() stores it to infoservice. The two steps will allow 
    some manipulation of the object by the client, or calling user. 
    
    -- Oriented toward exposing only valid operations to external
    user (portal, resource tool, or admin CLI client). 
    
    -- Direct manipulations of stored information in the infoservice is only done by Entity objects, not
    client user.
        
    -- Store method (inside of storeX methods) takes infoclient arg in order to allow multiple infoservice instances in the future. 
        
    '''
    
    def __init__(self, config):
        self.config = config
        self.ic = infoclient.InfoClient(self.config)
        self.log = logging.getLogger() 


    # User methods

    def defineUser(self,   
                   name,
                   first,
                   last,
                   email,
                   institution):           
        '''
       Defines a new User object for usage elsewhere in the API. 
              
       :param str name: The unique VC3 username of this user
       :param str first: User's first name
       :param str last: User's last name
       :param str email: User's email address
       :param str institution: User's intitutional affiliation or employer
       :return: User  A valid User object
       
       :rtype: User        
        '''
        u = User( name, first, last, email, institution)
        self.log.debug("Creating user object: %s " % u)
        return u
    
        
    def storeUser(self, user):
        '''
        Stores the provided user in the infoservice. 
        
        :param User u:  User to add. 
        :return: None
        '''
        user.store(self.ic)
        
                       
    def updateUser(self, user ):
        '''
        
        '''
        pass
    

    def listUsers(self):
        '''
        Returns list of all valid users as a list of User objects. 

        :return: return description
        :rtype: List of User objects. 
        
        '''
        docobj = self.ic.getdocumentobject('user')
        ulist = []
        try:
            for u in docobj['user'].keys():
                    s = "{ '%s' : %s }" % (u, docobj['user'][u] )
                    nd = {}
                    nd[u] = docobj['user'][u]
                    uo = User.objectFromDict(nd)
                    ulist.append(uo)
                    js = json.dumps(s)
                    ys = yaml.safe_load(js)
                    a = ast.literal_eval(js) 
                    #self.log.debug("dict= %s " % s)
                    #self.log.debug("obj= %s " % uo)
                    #self.log.debug("json = %s" % js)
                    #self.log.debug("yaml = %s" % ys)
                    #self.log.debug("ast = %s" % a)
                    #print(uo)
        except KeyError:
            pass
        return ulist

    def getUser(self, username):
        ulist = self.listUsers()
        for u in ulist:
            if u.name == username:
                return u
    
    # Project methods
    
    def defineProject(self, name, owner, members):
        '''
        Defines a new Project object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this project
        :param str owner:  The VC3 user name of the owner of this project
        :param List str:  List of VC3 user names of members of this project.  
        :return: Project  A valid Project object
        :rtype: Project        
        '''
        p = Project( name, owner, members = None)
        self.log.debug("Creating project object: %s " % p)
        return p
    
    
    def storeProject(self, project):
        '''
        Stores the provided project in the infoservice. 
        
        :param Project project:  Project to add. 
        :return: None
        '''
        self.log.debug("Storing project %s" % project)
        project.store(self.ic)
        self.log.debug("Done.")
    
    
    def updateProject(self):
        pass
    
    def addUserToProject(self, project, user):
        '''
        :param str project
        :param str user
        
        
        '''
        self.log.debug("Looking up user %s project %s " % (user, project))
        pdocobj = self.ic.getdocumentobject('project')
        udocobj = self.ic.getdocumentobject('user')
        # confirm user exists...
        pd = pdocobj['project'][project]
        po = Project.objectFromDict(pd)
        self.log.debug("Adding user %s to project object %s " % (user, po))
        po.addUser(user)
        self.storeProject(po)        

    
    def listProjects(self):
        docobj = self.ic.getdocumentobject('project')
        plist = []
        try:
            for p in docobj['project'].keys():
                    s = "{ '%s' : %s }" % (p, docobj['project'][p] )
                    nd = {}
                    nd[p] = docobj['project'][p]
                    po = Project.objectFromDict(nd)
                    plist.append(po)
                    js = json.dumps(s)
                    ys = yaml.safe_load(js)
                    a = ast.literal_eval(js) 
                    #self.log.debug("dict= %s " % s)
                    #self.log.debug("obj= %s " % uo)
                    #self.log.debug("json = %s" % js)
                    #self.log.debug("yaml = %s" % ys)
                    #self.log.debug("ast = %s" % a)
                    #print(uo)
        except KeyError:
            pass
        
        return plist
    
    
    def getProject(self, projectname):
        plist = self.listProjects()
        for p in plist:
            if p.name == projectname:
                return p
    
        
        # Resource methods    
    def defineResource(self, name, 
                             owner, 
                             resourctype, 
                             accessmethod, 
                             accessflavor, 
                             gridresource, 
                             mfa=False, 
                             attributemap=None):
        '''
        Defines a new Resource object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this resource
        :param str owner:  The VC3 user name of the owner of this project
        :param str resourcetype,  # grid remote-batch local-batch cloud
        :param str accessmethod,  # ssh, gsissh,  
        :param str accessflavor,  # htcondor-ce, slurm, sge, ec2, nova, gce
        :param gridresource,      # http://cldext02.usatlas.bnl.gov:8773/services/Cloud  | HTCondorCE hostname             
        :param Boolean mfa        # Does site need head-node factory?
        :param Dict attributemap: # Arbitrary attribute dictionary.      
        :return: Resource          A valid Project object
        :rtype: Resource        
        
        '''
        r = Resource( name, owner, attributemap )
        self.log.debug("Creating Resource object: %s " % r)
        return r
    
    
    def storeResource(self, resource):
        resource.store(self.ic)
    
    def ListResources(self):
        docobj = self.ic.getdocumentobject('resource')
        rlist = []
        try:
            for p in docobj['resource'].keys():
                    s = "{ '%s' : %s }" % (p, docobj['resource'][p] )
                    nd = {}
                    nd[p] = docobj['project'][p]
                    po = Project.objectFromDict(nd)
                    rlist.append(po)
                    js = json.dumps(s)
                    ys = yaml.safe_load(js)
                    a = ast.literal_eval(js) 
        except KeyError:
            pass
       
        return rlist
    
    def defineAllocation(self, user, resource, type, attributemap=None):
        '''
          
               
        
        '''
        pass
    
    
    def storeAllocation(self, allocation):
        allocation.store(self.ic)
        

    def listAllocations(self):
        pass
    
    def addAllocationToProject(self, allocation, projectname ):
        pass
        
    def defineCluster(self, name, ):
        pass
    
    def storeCluster(self, cluster):
        pass
    
    def listClusters(self):
        pass


    def defineRequest(self, name, cluster, environment, allocations, policy ):
        '''
        
        :return Request
        
        '''
        pass
    
    def storeRequest(self):
        pass

    def listRequests(self):
        pass

    # User-triggered action calls

    def saveRequestAsBlueprint(self, requestid, label):
        pass
    
    def listBlueprints(self, project):
        '''
        Lists blueprints that this project contains.
        '''
        pass

    def getBlueprint(self, name):
        '''
        :return Request
        '''
 


    
    
class EntityExistsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


