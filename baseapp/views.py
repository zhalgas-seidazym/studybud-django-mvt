from django.shortcuts import render


rooms = [
    {
        'id': 1,
        'name': 'Lets learn django!'
    },
    {
        'id': 2,
        'name': 'Lets learn frontend!'
    },
    {
        'id': 3,
        'name': 'Lets learn python!'
    },
]


def home(request):
    context = {'rooms': rooms}
    return render(request, 'baseapp/home.html', context)

def room(request, pk):
    room = [x for x in rooms if int(pk) == x['id']]
    room = room[0]
    print(room)
    context = {'room': room}
    return render(request, 'baseapp/room.html', context)
