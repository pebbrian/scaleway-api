import requests
import json
import os
from models.registry.image import Image
from models.pagination import Pagination
from .scaleway_api import ScalewayAPI
from pydantic import validate_arguments, ValidationError


class ScalewayRegistryAPI(ScalewayAPI):

    def __init__(self, region: str="fr-par"):
        super().__init__(name="registry", version="v1", region=region)

    ### IMAGES ###

    @validate_arguments
    def list_images(
        self,
        name: str=None,
        pagination: Pagination=Pagination(),
        ordering: Image.Ordering=Image.Ordering(),
        application_id: str=None,
        organization_id: str=None,
        project_id: str=None):
        return [ Image(**data) for data in json.loads(
            self.request(f"/images", data={
                "application_id": application_id, "organization_id": organization_id, "project_id": project_id, "name": name} | pagination.dict() | ordering.dict()))["images"] ]

    @validate_arguments
    def get_image(self, id: str):
        return Image(**json.loads(self.request(f"/image/{id}")))

    @validate_arguments
    def update_image(self, image: Image):
        return Image(**json.loads(self.request(f"/image/{image.id}", method="PATCH", data=image.dict())))

    @validate_arguments
    def delete_image(self, image: Image):
        return Image(**json.loads(self.request(f"/images/{image.id}", method="DELETE", data=image.dict())))