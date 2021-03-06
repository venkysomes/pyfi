from .wiggle import Entity
from fifo.helper import *


user_fmt = {
    'uuid':
    {'title': 'UUID', 'len': 36, 'fmt': "%36s", 'get': lambda e: d(e, ['uuid'])},
    'name':
    {'title': 'Name', 'len': 10, 'fmt': "%-10s", 'get': lambda e: d(e, ['name'])},
    'groups':
    {'title': 'Groups', 'len': 10, 'fmt': "%-10s", 'get': lambda e: str(d(e, ['groups']))},
    'orgs':
    {'title': 'Orgs', 'len': 10, 'fmt': "%-10s", 'get': lambda e: str(d(e, ['orgs']))},
}



def user_create(args):
    if not args.password:
        print "You have to specify a passwrod"
        exit(1)

    wiggle = args.endpoint._wiggle

    reply = args.endpoint.create(args.name, args.password)

    if reply:
        if args.organization:
            args.endpoint.join_org(reply["uuid"], args.organization)
        print "User " + reply["uuid"] + " created successfully."
    else:
        print "Faied to create VM."

def user_delete(args):
    args.endpoint.delete(args.endpoint.uuid_by_name(args.uuid))

class User(Entity):
    def __init__(self, wiggle):
        self._wiggle = wiggle
        self._resource = "users"

    def create(self, name, password):
        return self._post({"user": name,
                           "password": password})

    def join_org(self, uuid, org):
        return self._put_attr(uuid, "orgs/" + org, {})

    def make_parser(self, subparsers):
        parser_users = subparsers.add_parser('users', help='user related commands')
        parser_users.set_defaults(endpoint=self)
        subparsers_users = parser_users.add_subparsers(help='user commands')
        parser_users_list = subparsers_users.add_parser('list', help='lists users')
        parser_users_list.add_argument("--fmt", action=ListAction,
                                       default=['uuid', 'name'])
        parser_users_list.add_argument("-H", action='store_false')
        parser_users_list.add_argument("-p", action='store_true')
        parser_users_list.set_defaults(func=show_list,
                                       fmt_def=user_fmt)
        parser_users_get = subparsers_users.add_parser('get', help='gets a user')
        parser_users_get.add_argument("uuid")
        parser_users_get.set_defaults(func=show_get)
        parser_users_delete = subparsers_users.add_parser('delete', help='gets a user')
        parser_users_delete.add_argument("uuid")
        parser_users_delete.set_defaults(func=show_delete)
        # fifo users create bill -p pass -g group -o org
        parser_users_create = subparsers_users.add_parser('create', help='creates a new user')
        parser_users_create.add_argument("name",
                                         help="Name of the user")
        parser_users_create.add_argument("--password", "-p",
                                         help="Password of the user.")
        parser_users_create.add_argument("--group", "-g",
                                         help="Group of the user.")
        parser_users_create.add_argument("--organization", "-o",
                                         help="Organization of the user.")
        parser_users_create.set_defaults(func=user_create)
        parser_users_delete = subparsers_users.add_parser('delete', help='deletes a user')
        parser_users_delete.add_argument("uuid",
                                         help="uuid of VM to show")
        parser_users_delete.set_defaults(func=user_delete)
        
