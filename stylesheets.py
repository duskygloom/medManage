# dark mode

windowdark = '''color: white;
background-color: rgb(33, 33, 33);'''

addfielddark = '''border-radius: 15;
background-color: rgba(211, 215, 207, 50);
padding-left: 10;
padding-right: 10;'''



# light mode

windowlight = '''color: rgb(33, 33, 33);
background-color: white;'''


addfieldlight = ''''''


# both modes

addboxboth = '''background-color: transparent'''

topbuttonboth = '''QPushButton::hover
{
    font-weight: 700;
    color: rgb(255, 100, 125);
}
QPushButton
{
    border-style: none;
    background-color: transparent;
    border-radius: 20;
}'''

topbuttonselectedboth = '''\
QPushButton::hover
{
	font-weight: 700;
	color: rgb(255, 100, 125);
}
QPushButton
{
    border-style: none;
    background-color: rgba(127, 33, 128, 100);
    border-radius: 20;
}'''

topbarboth = '''border-radius: 30;
background-color: transparent;
border-style: solid;
border-width: 3;
border-color: rgb(255, 100, 125);'''

addlabelboth = '''font-size: 50pt;
font-weight: 700;
color: rgb(255, 100, 125)'''
