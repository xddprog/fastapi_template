from pydantic import BaseModel, EmailStr



class RegisterForm(BaseModel):
    username: str
    password: str
    email: EmailStr


class LoginForm(BaseModel):
    email: EmailStr
    password: str
