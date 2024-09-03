from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from app.utils.database import User, Organization
from typing import Dict, Any

class UserData:
    def __init__(self, db: Session):
        self.db = db

    def modify_record(self, table: str, action: str, **kwargs: Any) -> Dict[str, str]:
        if table == "organization":
            if action == "insert":
                existing_record = self.db.query(Organization).filter(Organization.name == kwargs.get('name')).first()
                if existing_record:
                    raise HTTPException(status_code=400, detail="Organization already exists")
                record = Organization(**kwargs)
                self.db.add(record)
            elif action == "update":
                record = self.db.query(Organization).filter(Organization.name == kwargs['name']).first()
                if record:
                    record.category = kwargs.get('category', record.category)
                    record.logo_link = kwargs.get('logo_link', record.logo_link)
                else:
                    raise HTTPException(status_code=404, detail="Organization not found")
            elif action == "delete":
                record = self.db.query(Organization).filter(Organization.name == kwargs['name']).first()
                if record:
                    self.db.delete(record)
                else:
                    raise HTTPException(status_code=404, detail="Organization not found")
            else:
                raise HTTPException(status_code=400, detail="Invalid action for Organization")
        elif table == "user":
            if action == "insert":
                existing_record = self.db.query(User).filter(User.name == kwargs.get('name')).first()
                if existing_record:
                    raise HTTPException(status_code=400, detail="User already exists")
                record = User(**kwargs)
                self.db.add(record)
            elif action == "update":
                record = self.db.query(User).filter(User.name == kwargs['name']).first()
                if record:
                    record.location = kwargs.get('location', record.location)
                    record.organization_name = kwargs.get('organization_name', record.organization_name)
                    record.profile_pic = kwargs.get('profile_pic', record.profile_pic)
                else:
                    raise HTTPException(status_code=404, detail="User not found")
            elif action == "delete":
                record = self.db.query(User).filter(User.name == kwargs['name']).first()
                if record:
                    self.db.delete(record)
                else:
                    raise HTTPException(status_code=404, detail="User not found")
            else:
                raise HTTPException(status_code=400, detail="Invalid action for User")
        else:
            raise HTTPException(status_code=400, detail="Invalid table")

        self.db.commit()
        return "success"
