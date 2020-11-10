import vk_api
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import LOGIN, PASSWORD

vk_session = vk_api.VkApi(LOGIN, PASSWORD)
vk_session.auth()

vk = vk_session.get_api()

user_groups_all = vk.groups.get(extended=1, fields=['members_count'])['items']
user_groups_100 = []
for item in user_groups_all:
    try:
        if item['members_count'] <= 100:
            user_groups_100.append(item)
    except KeyError:
        response = 'Невозможно отобразить число участников группы'
print(user_groups_100)

all_members = []
for item in user_groups_100:
    all_members.extend(vk.groups.getMembers(group_id=item['id'],
                                            fields=['sex', 'bdate'])['items'])

members_men_20_25 = []
today = datetime.today()
for member in all_members:
    if member['sex'] == 2:
        try:
            if len(member['bdate']) >= 8:
                bdate = datetime.strptime(member['bdate'], '%d.%m.%Y')
                age = relativedelta(today, bdate).years
                if 20 <= age <= 25:
                    members_men_20_25.append(member)
        except KeyError:
            response = 'Невозможно отобразить дату рождения пользователя'

df = pd.DataFrame(members_men_20_25)
df.to_html('templates\go_to_web\men_20_25_vk.html')
