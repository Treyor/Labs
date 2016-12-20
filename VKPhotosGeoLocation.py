import vk
import time

print ('VK Photos geo location')

session = vk.Session('b4f301da1e144a9e494a18cf139ea2a569c15a3e654eb18a8e5688eb270f6d86e038ec36f30b57d3e41cc')

api = vk.API(session)

friends = api.friends.get()

friends_info = api.users.get(user_ids=friends)

for friend in friends_info:
    print('ID: %s Имя: %s %s' % (friend['uid'], friend['last_name'], friend['first_name']))
print (len(friends))
print (friends)

geolocation = []
for id in friends:
    print('Получаем данные пользователя: %s' % id)
    albums = api.photos.getAlbums(owner_id=id)
    print('\t...альбомов %s...' % len(albums))
    for album in albums:
        try:
            photos = api.photos.get(owner_id=id, album_id=album['aid'])
            print('\t\t...обрабатывает фотографии альбома...')
            for photo in photos:
                if 'lat' in photo and 'long' in photo:
                    geolocation.append((photo['lat'], photo['long']))
                print('\t\t...найдено %s фото...' % len(photos))
        except:
            pass
        time.sleep(1)
    time.sleep(1)

js_code = ""

for loc in geolocation:
    js_code += 'new google.maps.Marker({ position: {lat: %s, lng: %s}, map: map }); \n' % (loc[0], loc[1])
    html = open('map.html').read()
    html = html.replace('/* PLACEHOLDER */', js_code)
    f = open('VKPhotosGeoLocation.html', 'w')
    f.write(html)
    f.close()
