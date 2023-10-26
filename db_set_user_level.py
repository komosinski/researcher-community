from open_science import db
from open_science.models import User, PrivilegeSet
import sys

def set_privilege():

    try:
        args_num = len(sys.argv)
        if args_num != 3:
            raise Exception('Invalid number of arguments, try:\ndb_set_user_level.py <user_id> <privilege_level>')

        user_id = int(sys.argv[1])

        user = User.query.filter(User.id == user_id).first()
        if user is False:
            raise Exception(f"User with id {user_id} does not exists")
        
        privilege_level = sys.argv[2]

        # user can provide privilege ID or name
        if privilege_level.isnumeric():
            privilege_set = PrivilegeSet.query.filter(PrivilegeSet.id == int(privilege_level)).first()
        else:
            privilege_set = PrivilegeSet.query.filter(PrivilegeSet.name == privilege_level).first()
        
        if user is None:
            raise Exception(f'User with id {user_id} does not exists')
        
        if privilege_set is None:
            raise Exception(f'Privilege "{privilege_level}" does not exists')
        
        user.rel_privileges_set = privilege_set
        db.session.commit()
        print(f"user's {user_id} privilege level has been changed to {privilege_level}")
    except Exception as ex:
        print(ex)

set_privilege()
