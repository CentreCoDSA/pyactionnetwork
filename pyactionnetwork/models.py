#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .api import ActionNetworkAPI

class ANBaseModel:
    def __init__(self, data):
        """Parses a json response into new instance, assigning values to class
        variables"""
        for (key, val) in data.items():
            setattr(self, key.replace('action_network:', ''), data.get(key, None))
        self.__json = data

        if len(self.identifiers) == 1:
            self.id = self.identifiers[0].replace('action_network:', '')
        else:
            self.id = [ident.replace('action_network:', '') for ident in self.identifiers]


class Form(ANBaseModel):
    """Represents a single form"""

    def __init__(self, data, *, api=None):
        # The Form model needs a handle to the existing API object so it can
        # query the submissions. 
        if api is None:
            raise TypeError("api cannot be None")

        super().__init__(data)
        self.__submissions = api.get_form_submissions(self.id)

    @property
    def submissions(self):
        return self.__submissions


    def __repr__(self):
        return "Form(id: {0}, title: {1}, total_submissions:{2})".format(
                    self.id,
                    self.title,
                    self.total_submissions
                )


class Person(ANBaseModel):
    """Represents a single person"""

    @classmethod
    def from_id(cls, person_id, *, api=None):
        if api is None:
            raise TypeError("api cannot be None")

        data = api.get_person(person_id=person_id)
        return cls(data)


    def __repr__(self):
        return "Person(id: {0}, name: {1})".format(
            self.id, 
            self.given_name + ' ' + self.family_name
        )
