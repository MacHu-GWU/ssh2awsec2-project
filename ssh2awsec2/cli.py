# -*- coding: utf-8 -*-

import fire
from . import api
import boto3
from simple_aws_ec2.api import Ec2Instance

class Config:
    def show(self):
        config = api.Config.read()
        print(config.to_json())

    def set_profile(self, profile: str):
        pass


class Command:
    def __init__(self):
        self.config = Config()

    def ssh(self):
        ec2_client = boto3.client("ec2")
        ec2_inst_list = Ec2Instance.query(
            ec2_client=ec2_client,
            filters=[
                # dict(
                #     Name="instance-state-name",
                #     Values=[
                #         "running",
                #     ],
                # )
            ],
        ).all()
        key = "SSH"
        # print(ec2_inst_list)
        choices = dict()
        for ec2_inst in ec2_inst_list:
            inst_id = ec2_inst.id
            name = ec2_inst.tags.get("Name", "no name")
            pub_ip = ec2_inst.public_ip
            choice = f"id = {inst_id}, name = {name}, public ip = {pub_ip}"
            choices[inst_id] = choice

        list_choices = api.ListChoices(key=key)
        inst_id, choice = list_choices.ask(
            name="ec2_inst",
            message="What EC2 you want to SSh to?",
            choices=choices,
            merge_selected=False,
        )
        print("selected: ", choice)

def main():
    fire.Fire(Command)
