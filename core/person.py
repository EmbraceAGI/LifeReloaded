import copy
import json
import random

cities = [
    '北京',
    '上海',
    '天津',
    '重庆',
    '哈尔滨',
    '长春',
    '沈阳',
    '呼和浩特',
    '石家庄',
    '太原',
    '西安',
    '济南',
    '乌鲁木齐',
    '西宁',
    '兰州',
    '郑州',
    '南京',
    '武汉',
    '杭州',
    '合肥',
    '福州',
    '南昌',
    '长沙',
    '贵阳',
    '广州',
    '昆明',
    '南宁',
    '海口'  # '拉萨', '成都', '台北', '香港', '澳门'
]

ages = [num for num in range(5, 11)]

genders = ['男', '女']

mbti_types = [
    'INTJ', 'INTP', 'INFJ', 'INFP', 'ISTJ', 'ISTP', 'ISFJ', 'ISFP', 'ENTJ',
    'ENTP', 'ENFJ', 'ENFP', 'ESTJ', 'ESTP', 'ESFJ', 'ESFP'
]

attribute_template = {'魅力': 10, '智力': 10, '健康': 10, '富裕': 10, '幸福度': 10}


def random_normal(minimum=1, maximum=10):
    mean = 4
    std_dev = 1.5

    num = random.gauss(mean, std_dev)
    rounded_num = round(num)
    clipped_num = max(minimum, min(maximum, rounded_num))

    return clipped_num


def initialize():
    city = random.choice(cities)
    age = random.choice(ages)
    gender = random.choice(genders)
    mbti_type = random.choice(mbti_types)
    attribute = copy.deepcopy(attribute_template)
    for attribute_name in attribute:
        attribute[attribute_name] = random_normal(1, attribute[attribute_name])

    return city, age, gender, mbti_type, attribute


class Person:

    STAGES = {
        'Childhood (5-12)': [
            'Individual Growth', 'Initial Education', 'Family Role',
            'Social Basics', 'Gender Cognition', 'Moral Concepts',
            'Cultural Exposure', 'Safety and Risks',
            'Entertainment and Interests', 'Mental Health'
        ],
        'Adolescence (13-19)': [
            'Identity Formation', 'Education and Career Planning',
            'Love and Sex Education', 'Friends and Social Circles',
            'Family Changes', 'Life Skills',
            'Social Responsibility and Citizenship', 'Mental Health',
            'Healthy Living and Habits', 'Money Management'
        ],
        'Early Adulthood (20-39)': [
            'Career Choice and Development', 'Partner and Marriage',
            'Social Network', 'Financial Independence', 'Self-realization',
            'Work-Life Balance', 'Social and Cultural Engagement',
            'Family Expansion', 'Global Awareness', 'Health and Lifestyle'
        ],
        'Middle Age (40-59)': [
            'Career Stability or Transition',
            'Children’s Education and Growth', 'Financial Planning',
            'Family Dynamics', 'Quality of Life',
            'Social Status and Influence', 'Health Management',
            'Psychological Adjustment', 'Social Maintenance',
            'Legacy and Heritage'
        ],
        'Old Age (60-90)': [
            'Retirement Life', 'Health and Medical', 'Family and Social',
            'Financial Security', 'Mental Health',
            'Personal Interests and Hobbies', 'Culture and Education',
            'Social Participation', 'Life Reflection',
            'Spirituality and Belief'
        ]
    }

    def __init__(self) -> None:
        city, age, gender, mbti_type, attribute = initialize()
        self.city = city
        self.age = age
        self.gender = gender
        self.mbti_type = mbti_type
        self.attribute = attribute

    def get_event_by_age(self, age: int = None) -> str:
        if age is None:
            age = self.age
        # Determine the life stage based on the age
        if 5 <= age <= 12:
            stage = 'Childhood (5-12)'
        elif 13 <= age <= 19:
            stage = 'Adolescence (13-19)'
        elif 20 <= age <= 39:
            stage = 'Early Adulthood (20-39)'
        elif 40 <= age <= 59:
            stage = 'Middle Age (40-59)'
        elif 60 <= age <= 90:
            stage = 'Old Age (60-90)'
        else:
            return 'Age out of range'

        # Randomly select an event from the corresponding life stage
        event = random.choice(self.STAGES[stage])
        event_prompt = '### 人生事件类型: \n' \
            f'\t **{event}**'
        return event_prompt

    def __str__(self) -> str:
        person_prompt = {
            '性别': self.gender,
            '城市': self.city,
            '年龄': self.age,
            '性格': self.mbti_type,
            '属性': self.attribute
        }
        return json.dumps(person_prompt)


if __name__ == '__main__':
    city, age, gender, mbti_type, attribute = initialize()
    print(f'city: {city}, age: {age}, gender: {gender}, mbti: {mbti_type}')
    print(f'{attribute}')
    print()

    person = Person()
    print(person)
