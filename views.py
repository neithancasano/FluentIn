from django.shortcuts import render, HttpResponse
import sounddevice as sd
import soundfile as sf
import numpy as np
import openai
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import requests
import re
from colorama import Fore, Style, init
import datetime
import base64
from pydub import AudioSegment
from pydub.playback import play
from navertts import NaverTTS
import random

# We need this to call some python code from the template directly
from django.http import JsonResponse

def get_new_word(request):

    print("get_new_word")
    
    api_key = "2"

    def chatgpt(api_key, conversation, chatbot, 
    user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
      openai.api_key = api_key
      conversation.append({"role": "user","content": user_input})
      messages_input = conversation.copy()
      prompt = [{"role": "system", "content": chatbot}]
      messages_input.insert(0, prompt[0])
      completion = openai.ChatCompletion.create(
          # model="gpt-3.5-turbo-0613",
          model="gpt-4",
          temperature=temperature,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty,
          messages=messages_input)
      chat_response = completion['choices'][0]['message']['content']
      conversation.append({"role": "assistant", "content": chat_response})
      return chat_response
      
    # gptresponse = chatgpt(api_key, conversation1, chatbot1, user_message)  
    word = chatgpt(api_key, 
                    [], 
                    ' Hello, G. I need a list of lists that follow this format (Pythonic list). [["당겨요", "pulls"],["문을 당겨요.", "Pull the door."], ["그는 내 손을 당겨요.", "He pulls my hand."], ["끈을 당겨요.", "Pull the string."],["당겨요와 밀어요는 반대입니다.", "Pull and push are opposites."],["낚싯줄을 당겨요.", "Pull the fishing line."]] The first list inside the big list is a Korean base word with their corresponding English translation. The succeeding five lists inside the big list are korean sentences (that use the base korean word) and their corresponding translations.I am passing this to a working code so please just give me the Pythonic list and nothing else. Do not add any dialogue. Just return the Python list only. do not say anything before the list and after', 
                    "")
    
    return JsonResponse({'word': word})

def home(request):

    # test if Naver is functioning correctly.
    '''
    tts = NaverTTS('안녕하세요')
    tts.save('hello.mp3')
    
    correct = NaverTTS('맞아요')
    correct.save('correctkorean.mp3')
    
    wrong = NaverTTS('잘못해요')
    wrong.save('wrongkorean.mp3')
    '''
    
    
    # variable passing test (pass var from view to template)
    varfromview = 11
    '''

    '''
    
    L = [
        [["당겨요", "pulls"],
         ["문을 당겨요.", "Pull the door."],
         ["그는 내 손을 당겨요.", "He pulls my hand."],
         ["끈을 당겨요.", "Pull the string."],
         ["당겨요와 밀어요는 반대입니다.", "'Pull' and 'push' are opposites."],
         ["낚싯줄을 당겨요.", "Pull the fishing line."]],
        
        [["추천해요", "recommends"],
         ["이 식당을 추천해요.", "I recommend this restaurant."],
         ["그는 좋은 책을 추천해요.", "He recommends a good book."],
         ["어떤 음악을 추천해요?", "Which music do you recommend?"],
         ["여행지로 이곳을 추천해요.", "I recommend this place for a trip."],
         ["그 영화를 정말 추천해요.", "I really recommend that movie."]],
        
        [["희망해요", "hopes"],
         ["나는 그가 성공을 희망해요.", "I hope he succeeds."],
         ["희망해요 그것이 진실이다.", "I hope it's true."],
         ["모두가 행복을 희망해요.", "Everyone hopes for happiness."],
         ["그녀는 좋은 결과를 희망해요.", "She hopes for a good result."],
         ["우리는 더 나은 미래를 희망해요.", "We hope for a better future."]],
         
        [["나눠요", "shares, divides into pieces"],
         ["빵을 두 조각으로 나눠요.", "Divide the bread into two pieces."],
         ["그는 그의 경험을 나눠요.", "He shares his experience."],
         ["모든 것을 공평하게 나눠요.", "Share everything equally."],
         ["우리는 비밀을 나눠요.", "We share a secret."],
         ["케이크를 나눠요.", "Divide the cake."]],
         
        [["헷갈린", "confused"],
         ["나는 그 문제에 헷갈린.", "I'm confused about that issue."],
         ["많은 사람들이 그것에 헷갈린.", "Many people are confused about it."],
         ["그 지시사항은 헷갈린.", "The instructions are confusing."],
         ["그녀의 대답에 나는 헷갈린.", "I'm confused by her answer."],
         ["이 도로표시는 헷갈린.", "This road sign is confusing."]],
         
        [["느린", "slow"],
         ["이 컴퓨터는 정말 느린.", "This computer is really slow."],
         ["너의 반응이 너무 느린.", "Your response is too slow."],
         ["느린 거북이가 결국에 이겼다.", "The slow turtle won in the end."],
         ["그는 느린 걸음으로 걸었다.", "He walked with slow steps."],
         ["왜 네 차가 그렇게 느린?", "Why is your car so slow?"]],
        
        [["길쭉길쭉", "long"],
         ["그는 길쭉길쭉한 팔을 가지고 있다.", "He has long arms."],
         ["길쭉길쭉한 빵은 더 많이 먹는 것 같다.", "Long bread seems to eat more."],
         ["그 나무는 길쭉길쭉하게 자랐다.", "The tree grew long."],
         ["나는 길쭉길쭉한 양말을 좋아한다.", "I like long socks."],
         ["길쭉길쭉한 모양이 특징인데요.", "It is characterized by its long shape."]],
        
        [["낡은", "old-fashioned, worn-out"],
         ["낡은 책을 발견했다.", "I found an old-fashioned book."],
         ["그 낡은 옷을 아직도 입니까?", "Do you still wear that worn-out clothes?"],
         ["낡은 집은 많은 이야기를 가지고 있다.", "The old house has many stories."],
         ["나는 낡은 가방을 사용한다.", "I use a worn-out bag."],
         ["그는 낡은 모자를 썼다.", "He wore an old-fashioned hat."]],
         
        [["민성숙한", "immature"],
         ["그는 아직도 민성숙한 행동을 한다.", "He still acts immaturely."],
         ["민성숙한 태도는 문제를 일으킨다.", "Immature behavior causes problems."],
         ["그녀는 민성숙한 점이 있어.", "She has an immature side."],
         ["민성숙한 반응을 보이지 말아요.", "Don't show an immature response."],
         ["민성숙한 선택은 후회를 가져올 수 있다.", "An immature choice can bring regrets."]],
         
        [["외로운", "lonely, alone"],
         ["나는 오늘 외로운 느낌이다.", "I feel lonely today."],
         ["외로운 사람들을 위해 할 수 있는 게 뭐가 있을까?", "What can be done for lonely people?"],
         ["외로운 곳에서 시간을 보냈다.", "I spent time in a lonely place."],
         ["그는 항상 외로운 것 같아.", "He always seems lonely."],
         ["외로운 밤, 별을 보았다.", "On a lonely night, I saw the stars."]],
         
         [["커다란", "big"],
         ["커다란 산을 넘어서 왔어.", "I came over a big mountain."],
         ["그는 커다란 꿈을 가지고 있다.", "He has a big dream."],
         ["커다란 집에 살고 싶어.", "I want to live in a big house."],
         ["커다란 나무 아래에서 휴식을 취했다.", "I took a rest under the big tree."],
         ["커다란 소리로 웃었다.", "He laughed out loud."]],
        
        [["빛나는", "shiny"],
         ["빛나는 별들이 하늘에 보였다.", "Shiny stars appeared in the sky."],
         ["그녀의 눈은 빛나는 반짝임을 가지고 있었다.", "Her eyes had a shiny sparkle."],
         ["빛나는 보석을 발견했어.", "I found a shiny gem."],
         ["그 빛나는 표면은 매우 매력적이다.", "The shiny surface is very attractive."],
         ["빛나는 머리카락을 가진 아이를 보았어.", "I saw a child with shiny hair."]],
        
        [["무관심한", "apathetic, indifferent"],
         ["그는 무관심한 태도를 보였다.", "He showed an indifferent attitude."],
         ["무관심한 사람들이 많아져서 걱정이다.", "I'm worried because there are many apathetic people."],
         ["그녀는 나의 이야기에 무관심한 것 같았다.", "She seemed indifferent to my story."],
         ["무관심한 세상에서 살기 힘들다.", "It's hard to live in an apathetic world."],
         ["무관심한 반응에 실망했다.", "I was disappointed by the indifferent response."]],
         
        [["다친", "injured"],
         ["다친 손가락을 보여줬어.", "I showed my injured finger."],
         ["그는 자전거 사고로 다친 것 같아.", "He seems to have been injured in a bicycle accident."],
         ["다친 동물을 발견했다.", "I found an injured animal."],
         ["다친 부위를 소독해야 해.", "You need to disinfect the injured area."],
         ["그녀는 다친 다리로 걸어가려 했다.", "She tried to walk on her injured leg."]],
         
        [["반바지", "shorts"],
         ["여름에는 반바지를 자주 입는다.", "I often wear shorts in the summer."],
         ["반바지를 입은 소년이 뛰어갔다.", "The boy in shorts ran away."],
         ["새로운 반바지를 샀어.", "I bought new shorts."],
         ["반바지에 얼룩이 묻었어.", "There's a stain on the shorts."],
         ["반바지를 입기에는 너무 추운 것 같아.", "It seems too cold to wear shorts."]],
         
        [["발표회", "presentation"],
         ["발표회가 다음 주에 있습니다.", "The presentation is next week."],
         ["발표회를 위해 준비했어요.", "I prepared for the presentation."],
         ["발표회가 잘 진행됐다.", "The presentation went well."],
         ["그녀의 발표회는 매우 인상적이었다.", "Her presentation was very impressive."],
         ["발표회를 연기해야 할 것 같아요.", "I think we need to postpone the presentation."]],
        
        [["언덕", "hill"],
         ["언덕 위에 작은 집이 있어요.", "There's a small house on the hill."],
         ["언덕을 올라가면 바다가 보여요.", "You can see the sea when you climb the hill."],
         ["그는 언덕을 빠르게 내려왔다.", "He came down the hill quickly."],
         ["언덕 아래서는 피크닉을 했다.", "We had a picnic at the bottom of the hill."],
         ["언덕 위에서는 바람이 강해요.", "It's windy on top of the hill."]],
        
        [["교과서", "school textbook"],
         ["교과서를 책상 위에 두었어.", "I put the school textbook on the desk."],
         ["교과서에는 많은 정보가 있어요.", "The school textbook contains a lot of information."],
         ["새로운 교과서를 받았어요.", "I received a new school textbook."],
         ["교과서를 통해 많은 것을 배웠다.", "I learned a lot through the school textbook."],
         ["교과서는 학생들에게 필수적이다.", "The school textbook is essential for students."]],
         
        [["비용", "cost"],
         ["비용이 얼마인가요?", "How much is the cost?"],
         ["이 비용을 지불할 수 없어요.", "I can't afford this cost."],
         ["비용을 줄이고 싶어요.", "I want to reduce the cost."],
         ["비용은 중요한 요소입니다.", "Cost is an important factor."],
         ["비용이 포함되어 있나요?", "Is the cost included?"]],
         
        [["경계선", "border"],
         ["경계선을 넘지 마세요.", "Don't cross the border."],
         ["그는 경계선에 서 있었다.", "He stood on the border."],
         ["이것은 우리의 경계선입니다.", "This is our border."],
         ["경계선을 그렸어요.", "I drew a border."],
         ["경계선은 명확해야 합니다.", "The border should be clear."]],
         
        [["반려동물", "pet"],
         ["반려동물로 고양이를 키우고 있어요.", "I have a cat as a pet."],
         ["반려동물은 집에 활력을 줍니다.", "A pet brings vitality to the home."],
         ["우리 반려동물은 가족의 일원이에요.", "Our pet is a member of the family."],
         ["반려동물을 위한 상점을 방문했어요.", "I visited a store for pets."],
         ["그녀의 반려동물은 매우 귀여워요.", "Her pet is very cute."]],
        
        [["가격", "price"],
         ["이 상품의 가격은 얼마인가요?", "How much is the price of this product?"],
         ["가격이 너무 비싸요.", "The price is too expensive."],
         ["가격을 좀 내려줄 수 있나요?", "Can you lower the price a bit?"],
         ["가격 정보를 확인해 주세요.", "Please check the price information."],
         ["이 가격에는 세금이 포함되어 있나요?", "Is tax included in this price?"]],
        
        [["재단", "foundation"],
         ["이 재단은 자선 활동을 합니다.", "This foundation does charity work."],
         ["재단에 기부하고 싶어요.", "I want to donate to the foundation."],
         ["재단은 어떤 목적으로 설립되었나요?", "What is the purpose of establishing the foundation?"],
         ["재단에서 스폰서를 찾고 있어요.", "The foundation is looking for sponsors."],
         ["재단의 활동에 참여하고 싶어요.", "I want to participate in the foundation's activities."]],
         
        [["학장", "dean"],
         ["학장님께서 연설을 하실 것입니다.", "The dean will give a speech."],
         ["학장은 학교의 대표입니다.", "The dean is the representative of the school."],
         ["학장에게 미팅을 요청했어요.", "I requested a meeting with the dean."],
         ["학장의 결정을 존중해야 해요.", "We should respect the dean's decision."],
         ["학장님의 사무실은 어디인가요?", "Where is the dean's office?"]]
    ]
    '''
    for i in range(0,len(L)):
        for j in range (0, len(L[i])):
            # tts = NaverTTS(L[i][j][0])
            # tts.save('tts/L' + str(i) + str(j) + '.mp3')
    '''
    
    Litem = random.randint(0, 24)
    '''
    return render(request, 
                  "base.html", 
                  { 'vfv':varfromview, 
                    'gptresponse': gptresponse,
                    'word1': word1,
                    'word2': word2,
                    'word3': word3,
                    'key1': key1,
                    'key2': key2,
                    'key3': key3,
                    'L': L
                    }
                  )
    '''
    print("home")
    
    return render(request, 
                  "base.html", 
                  {'L': L,
                   'Litem': Litem,
                   'global_k': 0
                    }
                  )
              

        
