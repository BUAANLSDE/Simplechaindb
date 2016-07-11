struct User
{
	1:string id
	2:string name
	3:i32 sex
}

service UserService
{
	string whatIsName(1:string word)
	User userInfo(1:string id)
}