from langchain.text_splitter import RecursiveCharacterTextSplitter

content_list = [
    ('Bread😡😡😡, if you see this, try to have a butter day 😘\nit s okay if your posts don t get a lot of attention on here 😊 we all just trying to enjoy the game and share experiences about it. Maybe with a better mental attitude, you ll get more traffic 😊 glhf everyone', 'EN', 'JP'), 
    ('4.6 Achievements (Doables)\nI feel like I need to touch every kind of leafy greens aaaaaa\n\nI just haven t done these 2 achievements yet because they are version-locked.\n\n1. Like Waters Clear - Max the Statues in Fontaine\n2. Dew Song - Max Fountain of Lucine\n\nHow are the others  Achievement Hunting going? Good luck to all!~\n\nctto - NepNepping for the Nahida art.', 'EN', 'JP'), 
    ('day 333…\n…of kaveh not being on an event wish banner', 'EN', 'JP'), 
    ('Help, choice between bennett and xingqiu\nHello, I have a question. I will pull Arlecchino but I would like to build a team of Arlecchino, Ei, Nahida and lastly bennett or xingqiu. I don t know which of the two to choose. Because bennett adds 25% ATK to me and maybe even better support. But for xingqiu, I will do a lot of elemental reaction vaporization and others. Here I am posting photos of my build of all four characters. Just for Raiden, I need to exchange one artifact for EM. And other characters have specific artifacts that I won t change unless I need to raise ER or CRIT. So please someone advise me. Is it better to take Bennett or xingqiu to the team with arlecchino, ei, nahida? If you are interested, I would use Ei and Nahida for sub-dps, and Bennett or xingqiu for support. But I don t know if xingqiu support allows it, but probably yes. If so please correct me. I still don t know exactly what support does and how it converts dmg. I still have a CRIT DMG 3star weapon. Feel free to ask anything. Please give me advice.\n', 'EN', 'DE'), 
    ('i just wanted the remarkable chest and  this happens\nEven though I have already 100% explored the desert, I still have many unsolved puzzles. I even found Seelies to guide.\n\nAnyway, I will take them all as Father s primo funds.\n\n\n\nPS: i am aware that treasure chests or puzzles are plenty and  not the sole basis for exploration progress. 😆', 'EN', 'TH'), 
    ('How old is Arlecchino?\nFreminet knew the or a former head of the house. Does he mean the former knave by that or did Arlecchino let someone else run the house?I mean when she becomes the Knave only Capitano Signora and Scara are there......does that mean there only were 4-5 harbingers at that point?Or were the other on duty? ', 'EN', 'DE'), 
    ("Cute Acheron Wallpaper! (2 versions) \nHihi! Just sharing this Acheron wallpaper I made ♡ I made a regular version and her 2nd form version :D ! I love using her in Simulated Universe, she makes the runs so much more fun If you want to use this wallpaper too, you can download it from my Ko-fi for free ^^ Ko-fi link here, click me! ♡There's other character wallpapers there too if you want to see which other ones I made Acheron Wallpaper (normal ver.)Acheron Wallpaper (2nd form)", 'EN', 'TH'), 
    ('Bruh, their children look just like Aether\nJust some sweet VentixLumine art I found. I like the design of the children; they re not exactly like a carbon copy of the mom/dad like what I see with the Aether harem fan arts, but they still somehow managed to look like him. The genes are a great mix.\n\nArtist: @_mylazysister (X/twitter)', 'EN', 'VI'), 
    ('spiral abyss 9 stars\nany thoughts on these 2 teams?', 'EN', 'CHS'), 
    ('Dr. Ratio Save Me\nAcheron is surely strong, but this success must give credit to Dr. Ratio at 1st team. He gave more turns available for 2nd team.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'RU'), 
    ('Kaeya flirting\nsadly I couldn t take the ss of the best scene☹️😔', 'EN', 'CHS'), 
    ('saving on honkai star rail day 320\n4 more days until arlecchino I have 90 pulls and I m on 50 pity so I need to get lucky but I have a small chance if I lose 50/50 hope I don t though because I also want to pull for furina on her next rerun', 'EN', 'TH'), 
    ('Love all his silly expressions lol\nfirst post on here is gonna be welt lmao', 'EN', 'EN'), 
    ('Primogems\nWho streamers i should follow to get best redeem codes?? Allways ending up to see the codes when they expired already😅', 'EN', 'CHS'), 
    ('I’m Excited!\nI’m really excited to earn more primos. I don’t have a specific character I want this update so I’m hyped to work for characters I want!', 'EN', 'RU'), 
    ('Amplifying Test.\nIs it possible to win a beta ticket lmao.', 'EN', 'ID'), 
    ('Dan & Jing Yuan Team\nThis was before Aventurine came out. Now Gepard can go into retirement The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'JP'), 
    ('Abyss duo\nLoving these guys beating the abyss with me.', 'EN', 'JP'), 
    ('Aventurine WIP Build. In need of suggestions. (Read desc)\nObviously his build isn t finished, but I wanted some suggestions on what to aim for. Still farming for relics and all, going for a shielder dps. any advice? (Ahem, may also be an excuse for a post to get his background/wallpaper thingy)', 'EN', 'EN'), 
    ('Eula enjoying a peaceful day in Mondstadt\nI drew Eula in Procreate app but the background is AI generated. This is the first image I made like this. I lost motivation to drawing when I started to do a similar background from scratch. It would take too long at my level of skill. Maybe one day its possible.', 'EN', 'TH'), 
    ('Cosplay Drawing 👀\nI don t do cosplay but I always wanted to try it someday. But for now heres a drawing version of me in a Wriothesley cosplay 🤭 \n\np.s i hate coloring lol', 'EN', 'JP'), 
    ("0 Cycle | MoC 10 |  Chronicle of the White Nights Dream Kingdom\nFirst half was not too difficult. The second side though, holy f**king sh*t it took SOOOO many tries to shave this down to 0 cycles on Sam. I kept entering Cycle 1 with Sam at like 4% health. I asked a friend to take a look at my run and she suggested I drag out the first wave to fill Ultimates and replenish SP as well as holding the stronger attacks until the Memory Imprint is at a higher stack (enemies take more damage). Eternally grateful for her support! <3I didn't use my Acheron Ult in Wave 1. I was able to Acheron Ult twice on Sam as well as keep RM's Ult/Skill up in the entire second wave. Somehow it worked!!I tried to record my run this morning but maybe a skills issue, RNG (enemies' hits replenishing energy or where Crimson Knots land), or the fact that my Acheron doesn't crit 100% of the time (~90%CR in combat). Either way I'll probably post something later. Only my second time 0 cycling MoC10 and it felt surreal.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'FR'), 
    ('Sparkle 💖✨\nPics I found on Pinterest of sparkle 💖 \n\nThey are not mine I tried to find the artists the screenshots are at the end\n\n(⚠️not mine⚠️)', 'EN', 'JP'), 
    ("My mom likes huohuo sticker\nIn whatsapp I have huohuos stickers from in game and don't judge but I send them to my mom and now she uses them sometimes when talking to me...", 'EN', 'RU'), 
    ('I FINALLY FOUND THE ORIGINAL ARTIST FOR THESE ARTS YESSS\nthey also did the xiao and venti s birthday art, lyney and xiao s valentines/white day art too (and i forgot the rest)', 'EN', 'CHS'), 
    ('Oh\nI believe father will come home😤', 'EN', 'TH'), 
    ('Trying random character teams\nI was just messing around. I ended up playing with this team. This team is pretty fun to play.\n\nQuestion-\n\nJust want to see what others think of this combination of characters.\n \nDid you try this team?\nWhat are your thoughts?', 'EN', 'VI'), 
    ('Wishing for Adventurine\nSorry, Adventurine....\nIt seems, you won t be able to join my trailblazing journey this time....\n\nAND\n\nWelcome ....Bronya....\nLet our trailblazing journey begin.', 'EN', 'JP'), 
    ('The scenic path home\nInspired by all the cherry blossom pictures, I decided to try to make a scenic spot for my teapot. Hope you like it!\n\np.s. mhy pls gimme more load 🥲', 'EN', 'KR'), 
    ("Blade hypercarry & Daniel hypercarry\nDidn't think i'll make it in 10 turns but i managed first try! Nice to see i can still 3 star with older characters and without dot/acheron.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'CHS'), 
    ('Companionship Post\nLantern rite thing I forgot I took', 'EN', 'DE'), 
    ('chiori doll smile\nonly picture chiori doll smiling', 'EN', 'FR'), 
    ('itto and gorou\nNGL it s still one of my favourite ships, mainly because I love them both \U0001f979\nhonestly I love all the inazuma characters', 'EN', 'EN'), 
    ('CAT XIAO I WANT YOU\nWhy does xiao have to be cute like that ?', 'EN', 'EN'), 
    ('LYNEY\nFOUR DAYS TIL LYNEY IS BACK😭😭', 'EN', 'RU'), 
    ("I need a storytime\nHey y'all. I did not pay any attention to Wanderer's story. And I keep forgetting he is a harbinger. I dont have him as a playable character, so I cant just look at his story. Can someone help me out? Thank you!", 'EN', 'KR'), 
    ('Bagde...\nomfg why is my hubbie looks so smol', 'EN', 'ID'), 
    ('Serenitea Pot Shenanigans (4.5): Deportation\nWhile Kunimaru s involvement in the Illegal Primogem operation may not have been proven by Mondstadt s authorities, his antics had forced them to deport him back to Sumeru.\n\nHonorary Knight Aether had been given the task to escort the deportee back to Sumeru, leading to a certain conversation inspired by Hellsing Ultimate Abridged because of the date...', 'EN', 'JP'), 
    ("Gold and Gears all Conundrums finally\nIt took me like 5-6 attempts to rebeat this easiest boss. First I tried Topaz and Ratio but turned to March and Ratio, which is better because March can provide shield and freeze small bugs. I also let Ratio steal Topaz's light cone and changed to HP sphere because DMG increase is kind of plenty in SU. Anyway, Topaz + Ratio is good because they can break weakness of multiple bosses, but eventually you need a more specialized team. I also tried Dan Heng IL a few times (my DHIL is E2), but it turned out terrible for enimies without imaginary weakness. The thing with Gold and Gear is you don't always get Swarm for the final boss. ", 'EN', 'CHT'), 
    ('Guys what do I post I think I m going crazy\nAUGHHHHHBHHHHHHHBBHBHHHHHHHHHH erm what the sigma\n💀\n≤))≥\n_/ \\\\_erm what the sigma\n💀\n≤))≥\n_/ \\\\_erm what the sigma\n💀\n≤))≥\n_/ \\\\_', 'EN', 'FR'), 
    ("Wanderer never asked me to name him\nIs there any reasoning to this? I've finished the archon quest a few months back and I never got to name Wanderer. He didn't ask me, I never met him after that as well, straight up to Nahida explaining how the traveler is the fourth descender, I did Dainsleif one too then Fontaine quest began.I did Nahida's story quest thinking it'd be the issue but it certainly didn't fix it since Wanderer wasn't even there. It's pretty odd because everybody else gets to name him but I don't so I'm wondering if there's anything I accidentally left out or have not done?Edit : Found the problem guys thank you 😭🎀", 'EN', 'TH'), 
    ('Remainder !\nplz touch your grasses time to time', 'EN', 'CHT'), 
    ('Happy Birthday 🎂\nBought an ice cream cake for her. Found out it was Bakugou s birthday and also my cousin s fiancée s birthday.\n\nAlso Yelan is so pretty in her birthday pic 🥺', 'EN', 'RU'), 
    ('Bullack Swanhit\nwhy do people even shorten her name to BS?', 'EN', 'RU'), 
    ('How Do Y’all Think About This? (If U Know Meh Irl Don’t Look)\nMy b-days coming up and I’m trying to make custom invitation letters to each person, this specific person LOVES Dottore so yuh. \n\nHave a great day!', 'EN', 'DE'), 
    ('WHY????\nHoyolab won’t let me upload images at the current moment for some reason so gotta start my human tail uploads tomorrow ', 'EN', 'VI'), 
    ('4 types of people when being bribed:\nThe Briber: "I don\'t want your money!"& Bronya"Sure!"*kills on the spot* & Seele"I have plenty" *proceeds to flex there own money*', 'EN', 'EN'), 
    ('DanHeng IL s Ultimate\nNot sure how long is this in my Gallery ( ´∀｀)', 'EN', 'EN'), 
    ('Finally!\nGot him on pity 76, won the 50/50', 'EN', 'FR'), 
    ('never regrated anything more than leveling kazuha in this game\nin the first image, you can see when I got him, he is my first 5star, but I never liked him that much\njust for 28 more em on this dude, the cost is just not worth it, he was perfectly fine at level 80, I had to fight magu kenki 10 times for the matts pulse so much mora and hero wits\nI was told he be getting around 100 more em so I thought its worth it to get close to the ideal 1000em\nif I m missing something here please let me know, cuz I ve heard he s one of the units that must be level 90, but I say he s one of them that should not be more than 80, just hate wasting so much resources on him when I m broke all the time, I should have gone for diluc instead', 'EN', 'TH'), 
    ("hello im back for more useless himeko posts bc i need the pts\n im too lazy to answer the question so here's the very only 6 emojis of himeko in hoyolab i rly thought there'd be more", 'EN', 'TH'), 
    ('Progenitor fanart\nI’m never satisfied with how Mona turns out, but it’s done and I’m happy enough with that…The Progenitor series is so good, and I’m super slow but I had to draw the scrmn😭🙏', 'EN', 'TH'), 
    ('Ladies and gentlemen we have found klees sibling\nMay I present to you sparkle in a canon universe', 'EN', 'CHS'), 
    ('Pleasantly Surprised!\nI didn’t think I’d enjoy every characters play style as much as I am, if only I didn’t have the reaction time of a snail 🤣😅', 'EN', 'VI'), 
    ("Aventurine Banner Open post\nHe quickly became one of my favourite characters in the game and I just had to pull for his lightcone. He is the first actual character that I really wanted that came out! (others being Screwllum & Firefly) (Pulled DHIL cuz I needed a DPS, Sparkle for DHIL).(Not saying I don't want other characters, I find them cool but they aren't my favourites)", 'EN', 'JP'), 
    ("Neuvillette is homeeeeeee!!\nI was losing hope...like I pulled for him as soon as they dropped his banner but I didn't get him  so today, the last two days before they take down his banner, I decided to grind and get ten fates to try one last time and at pity 0BOOOMHE APPEARS!! I AM SO HAPPPYYY Now, I can say bye-bye to my luck for a bit but it was worth it", 'EN', 'RU'), 
    ('Is this normal or what?\nDoes this happen frequently or ? Like I’m grateful but i genuinely am surprised to see how many people actually achieve this stuff', 'EN', 'DE'), 
    ('Totally not obsessed\nI absolutely love his character and boss fight (even tho he killed my dps and had to restart). Cant wait for his nova desktop animated wallpaper.', 'EN', 'TH'), 
    ('Daily aventurine post!\nI js arrived in penacony..I’m tl 56..', 'EN', 'EN'), 
    ("[Daily Sharing] Feeling Lucky? Some Eventful Ley Line Overflow Rewards.\nI've been seriously pushing for Mora Ley Lines of late, so it was a nice change of pace when today's 3 Bonuses gave me 10 Hero Wits per Ley Line, as that is the maximum amount it can give per reward usually. Thank you kindly, good fortune! I will make good use of these! 1st Reward from Ley Line Overflow today.2nd Reward from Ley Line Overflow today.3rd and Final Reward from Ley Line Overflow today.It's important to use your resources wisely, at least, that's what I tell myself anyways. Regardless, that's all for today! Thanks for Viewing! Peace Out!! ", 'EN', 'CHT'), 
    ('got him!!!\nkinda sad i wanted acheron but yk it is what it is and also he’s not bad also i kinda knew that i wouldn’t get her so i still happy with this ', 'EN', 'RU'), 
    ('Buff herta\nIf cocolia freezes kafka, restart. Runs with this exact teams varied for me between 54-65k points. Took a lot of tries. Never give up. The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'EN'), 
    ('Whyyy😭😭\nI tried pulling for neuvillettes signature but got kazuhas sword😭😭. I lost every 50/50 on my account since playing bra😭', 'EN', 'CHS'), 
    ('Who hurt this person 😭\nI just wanted to use all my write bottles for the day on random notes and this person took one of my bottles way to personally. And i only made 1 bottle saying im happy with myself and they got mad about it, pretty funny, hope they are doing well.', 'EN', 'CHT'), 
    ('Istg if anything happens to Aventurine I will be the next Otto Apocalypse\nTHE TEXT I GOT NEXT DAY AFTER GETTING AVENTURINE HURTS SO MUCH WAHHHHH-\nI will never be healed after 2.1 (;´༎ຶД༎ຶ`)', 'EN', 'CHT'), 
    ('i’m not sure who to build\ni need to build more characters but i don’t know who or what line up would be good. i currently use stelle, dan heng, tingyun/march 7th, and huo huo.', 'EN', 'VI'), 
    ('🐈\u200d⬛ Pardo time! Some pics.\nI took videos but i hate that I can t post them there. It was so hot outside i was dying but i loved the pics. My official photos will be at Otakufest on Saturday. One of my friends are bringing Elysia so it will be so pretty to take pics with. I tried buying the Can plushie but no one is selling it. :( I hope you guys enjoy this cute pics. And thanks again for the support. I rlly want to cosplay Mobius tho. But she s so expensive.', 'EN', 'TH'), 
    ('Acheron/Jingliu hypercarry\nBoosted Nihility and overkilling Jingliu!The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'RU'), 
    ('Cant fast travel, else im stuck in the loading screen. Anyone have a solution for this? Using a pc btw\nThis issue just came up today, and to this day it was all fine then idk what happened. You can log in just fine, get into the game just fine, but then if you try to fast travel anywhere the loading screen will be just like that theres no progress increasing at all, and when you are finished doing a battle it will be the same except its a black screen, its been so long waiting and nothing happens. I already tried reinstalling the app, check all of my drivers and its all up to date, i tried changing my provider data, clear the cache, and its still the same. Do you guys have any solution please fix and give the solution fast. thank you!', 'EN', 'RU'), 
    ('neuvillette photos!\ni finally got neuvi after losing my 50/50', 'EN', 'JP'), 
    ('About seelie Columbina theory\nIf Columbina is a seelie canonically (and so can’t love) then canon can bite me because Arlebina is too cute to just disregard.Sorry not sorry.- someone who is usually canon &gt; fanon', 'EN', 'VI'), 
    ('I’ve come to the conclusion that..\nI’m straight but Arlecchino is an exception 😍', 'EN', 'JP'), 
    ('Sparkle Cake!!!!!!!\nI made one of my fav girl in hsr', 'EN', 'TH'), 
    ('Tighnari the healer\nIdk who to give the credits to so if you find the owner of the meme let me know !\nBut just I love this duo so much', 'EN', 'TH'), 
    ("How much Fragile Resins Do yall use when farming?\nI'm just curious how much yall have prepared or used for a character u wanna build &gt;< like around how many fragile resins have u spent on 1 character ? ", 'EN', 'CHS'), 
    ('DOT + Acheron Full Auto\nAuto did all the work this timeThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'DE'), 
    ('Happy Birthday Yelan!\nStylish, secretive, hydro bow user, Yelan. Happy Birthday!\nI love her playstyle and animations. Seeing her in a new event or giving her another story quest would be great.', 'EN', 'DE'), 
    ('Bronya is a great leader\nI’m sure some people wouldn’t understand the implications of giving away your freedom in exchange of “prosperity”\n\nThis is what happened in my country. What started was a good thing, ended in tragedy and the loss of the livelihood of the many— all because we believed in a superpower and didn’t believe in ourselves. And now we suffer and our children suffer. We owe the world bank more with each president. It’s outrageous. \n\nGames and many forms of fiction display reality. I’m quite happy with Bronya’s choice and I wish to see a follow up to Belobog’s rise.', 'EN', 'CHS'), 
    ('The future of Aventurine\nThe future of him is that I want him to be safe and sound and that nothing will happen to him and that he will meet up with his bestie Dr Ratio and everyone will live happily ever after. Sorry guys but I’m on copeium right now… a little drawing I did before of Ratio in my style.', 'EN', 'JP'), 
    ('An event from Honkai star rail mentioning Genshin\nVery unexpected but interesting to take note', 'EN', 'RU'), 
    ('memes review\nme with 32 fates wait for new banner', 'EN', 'KR'), 
    ('I just love Inazuma so much \nI m sad that I m getting closer to 100% in every area. It s so beautiful!\n\nI get so nostalgic for the Archon quest. I know some people have their reservations about it, but I thought it was fantastic!\n\nCannot pass by that statue without thinking of that scene with Thoma.\n\nAnyway, I did the thing!', 'EN', 'DE'), 
    ("Question about re-run banners if anyone knows.\nI'm new to gacha games as of last year when I started HSR. I wanted to get both topaz and aventurine for my Dr Ratio FuA team. However if I get aventurine now I most likely won't be able to pull on topaz re-run banner. If I get aventurine will I be able to pull for topaz in the future or do the characters only get 1 re-run ?", 'EN', 'JP'), 
    ('I made a bookmark!:)\nI redrew the first ever Genshin impact fanart I ever made as well❤️ If it guys want the bookmark yourself, feel free to tell me, and I ll give you a scan❤️ Otherwise I hope you all have a great evening❤️ (it s evening for me lol)', 'EN', 'CHT'), 
    ('Daily Adventurine post for companionship points!\nCurrently farming for his new build, wish me luck!', 'EN', 'RU'), 
    ('got a thing\nI had to get a new phone case, and I opted out of the wallet case I usually get to get something that will keep flour off my phone screen and out of my charge port. wasn t expecting it for another few days, so this was a nice surprise. idk where to put it, so I guess discussions will do. It s on Amazon, for other Wrio stans who might be interested.', 'EN', 'JP'), 
    ('YaeMiko maid cosplay\nA few selfies from my last session. \n\nOutfit: Yaemiko maid from Uwowo\n\n\n#cosplay #yaemiko #yaemikocosplay #genshinimpact #genshinimpactcosplay', 'EN', 'CHS'), 
    ('What s up with this?\nA friend of mine pointed this out and I thought it was post worthy. They look so similar so whats the deal with it? Same eyes, headband, and eyes that I can see. I guess we have to wait till 4.6 and see if this is talked about!', 'EN', 'RU'), 
    ('Don’t mind the title I’m feeling chatty today and I want to talk to people.\nI also want to give positive feedback to people ', 'EN', 'TH'), 
    ('AHAGSGSYAUA THEIR SO CUTE\nI LOVE CYNARI ♡♡♡♡♡ {not my art}', 'EN', 'DE'), 
    ("I NEED HELP GUYS\nI'm currently guranteed a 5 star on the limited banner in genshin with 42 pity and 8220 primogems.... The question is if I should pull C1 Neuvillete, Arlecchino, or a Furina. PLEASE GUYS I NEED HELP MAKING THIS DESCISION!!! (I also have a fully built amazing Hu Tao if that changes anyones opinion with Arlecchino.)", 'EN', 'FR'), 
    ('Did it with sampo cleared with 3 stars on exactly 20\nSampo: What are you waiting forAbuse the trottersThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'CHS'), 
    ('Some Aventurine memes~(PLEASE read description for those who follow me)\nOk this note is for my followers or those who expect more memes from me sooo i won t be posting for a month and a half or maybe less because my final exams are starting and i need to prepare for them(┬┬﹏┬┬). Of course, this doesn t mean I m leaving forever after I m back I ll try my best to post daily, and maybe I may come back to reply to comments（＾∀＾●）ﾉｼ and stuff soo that s it i yall have a wonderful day ヾ(•ω•`)o', 'EN', 'DE'), 
    ("Lyney or Arlechinno?\nPersonally, neither...The older characters are powerful AND simpler to use. Arlechinno and Lyney- while not rocket science- still seem to have self-concerned kits that make using them more of a hassle then the enemies you'll be using them against. I'm certainly looking forward to new Pyro characters. Arlechinno was the hope for a while, BUUUT she's a mixed blessing. Still waiting on the Pyro Archon, BUUUUT there's rumor that there's a very powerful Pyro character coming out...and it's a guy so cool because playing women all the time is irritating me. I think after Pyro Archon I'll just wait for characters that offer better and substantial improvements to my existing characters. For instance, if there's a Cryo character that deals good and consistent Cryo enough for better MELT teams, I think I'll pull for them if they are a 5 star. I'll never pull for 4 stars. Only exception is Archons. Gotta catch them all!!!", 'EN', 'CHS'), 
    ('Day 187 Saving for Chlorinde!\nExplored more of the Chasm, got to the 70%’s! Also did some chasm quests and leylines in Liyue for leveling materials! ', 'EN', 'KR'), 
    ('HELP ME REACH 1K‼️\nI been waiting to at least reach 1k for a while now I finally have been cosplaying for a year and a half now! More content will be coming out soon ‼️ thank you so much for all the support love you guys💕🌊', 'EN', 'JP'), 
    ('Getting an Achievement without the required character(s)?\nI don’t have Aventurine but… I somehow got this achievement. My characters in battle are Serval,Acheron,Herta,Natasha.', 'EN', 'VI'), 
    ("Seirai Island\nYou all said I should touch grass and I did it. See? I have placed the camera in the grass so you have the proof I did it.Mmmm grass.I started playing again star rail so you'll probably start seeing photos of it soon. Thought I still need to know better the places so I don't get post.I really would like they add the jump button.Bye everyone and see you tomorrow.", 'EN', 'CHS'), 
    ("My thoughts on the character skins that will be released on the 5.4 Lantern Rite, next year\nI believe the skins will increase in number once more next year to maybe four, five or six. The two characters I predict will get skins next year are: Zhongli and Xiao Zhongli is mainly because they have teased a character skin this year that was first shown during the story teaser during last year's lantern rite, so it's only natural that he'd get one.And for Xiao is because I still believe he'll get a skin and a character skin for him is in possibly in the pipeline. Previously, I thought Xingqiu, Beidou, Xiangling or Chongyun would get character skins alongside Xiao this year and mentioned this in a previous post. But only Xingqiu got one. Other characters that I can see possibly getting skins alongside them: Qiqi, Yelan, Yanfei, Baizhu, Yunjin, Hu Tao, Xiangling, Chongyun ", 'EN', 'KR'), 
    ('Sooo much horny weebs\nI’m surprised yet not surprised by the amount of followers I gained from just one post. Just goes to show that if u wanna grow your account substantially then post and mention thicc thighs. Where’s the no horny hammer when u need 🤣', 'EN', 'FR'), 
    ('Should “Aventurine” be “Kakavasha”?\nSPOILERS for 2.1!!!\xa0Just a random thought - is Aventurine still “Aventurine” after the ending of 2.1? Isn’t the aventurine stone destroyed, and his connection to it severed by Acheron? Plus it really seems like a lot of IPC employees are slaves (“forced employment”), definitely true for Topaz and Aventurine, so shouldn’t that name be abandoned if they’re freed/escape? I interpreted the discussion with Acheron as him being freed from both the IPC’s power and Sunday’s curse, and now finding himself a free man, with a future for himself to decide. (Providing he can survive the real dreamscape, but I’m fairly confident we can side with Ratio on this one. Do live, gambler - we’re betting on you!)\xa0Basically this boils down to wondering if we should call him Kakavasha out of respect? I guess we need to wait and see? Perhaps Aventurine himself sees Kakavasha as dead, so he might not want to use that name either. Not out of hatred or lack of love for his childhood, but the opposite actually. Maybe he feels too changed from Kakavasha to reclaim his birth name? ', 'EN', 'RU'), 
    ('My drawing\nNot Hoyoverse related but please support my art on Instagram, Youtube and Tiktok! <3 \n@yuanting_insta\n@yuanting_yt\n@yuanting_tiktok', 'EN', 'CHS'), 
    ('Sethos Art\nSethos art I finally finished 😆', 'EN', 'RU'), 
    ("Favorite places to meet Kaeya in game\nWhen you do his quest at the beginning of the game, he's just chilling in the headquarters and when the Sumeru quest was going on (him talking to the bird was hilarious like what are you doing good sir?) ", 'EN', 'JP'), 
    ('Stage 10\n✨Important Eidolons: E2 IL✨Key Stats: Cr CDThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'KR'), 
    ('Question about World Level\nI just ascended to WL 2 and found out, that my loot will now be better. Would id be wise then to save my keys for even higher WL or does it not affect these chests?', 'EN', 'DE'), 
    ('Baizhu Drawing\nThis is for the Stay Healthy art competition!\nAttached are the wips and screenshots of my layers!\nCritiques are welcome!\nDone on ibis paint', 'EN', 'TH'), 
    ('this fan art is so cowl bruh\nnot mine credits to the og artist', 'EN', 'JP'), 
    ('Kafka is beautiful\nShe is so beautiful, I would do anything for her', 'EN', 'VI'), 
    ('Yelannn b-day☆*:.｡. o(≧▽≦)o .｡.:*☆\nHappy birthday Yelan my pookie ╰(*´︶`*)╯♡', 'EN', 'RU'), 
    ('When you win your 50/50. (Topaz Edition)\nHow it feels when we win our 50/50.', 'EN', 'KR'), 
    ('all raidens I know\n4 versions of Raiden that I know', 'EN', 'RU'), 
    ("What sthe prettiest burst??\nI think it's either Ayatos or Neuvillette.", 'EN', 'CHS'), 
    ('Not Furina friendly\nI just want my Yelan to crit cause I just want to. And I met Xiaoven person and I personally don’t like it kinda, then I like them after I played a song of Moonlike Smile from Dragonspine. I appreciate your comment! (Comment all hates you want, I just can’t wait how many comments I will receive in such post)', 'EN', 'JP'), 
    ('Roomies\nHe would probably find me a weird person or interesting maybe both BUTTTTTTT we WILL have cuddle evenings/nights (slowburn he loves me i love him we get married and get kids (cats + yanqing) then we die old and happy together) I don’t accept an apartment without a balcony and if its a house then i wanna be able to climb on the roof because yes its fancyAll in all me as his roomie is basically me as his housewife and I don’t mind (i hate work, who doesnt)tho… unlwss modern au or sum he wouldnt need a roomie or whatever bc hes probably rich and can pay stuff for himself okokokk fksbfnd', 'EN', 'JP'), 
    ('Weekly Report Competition enters\nFollow, and comment on this post to enter! I will host another competition once Termi_nator can get on his phone. (Lol)', 'EN', 'CHT'), 
    ('DHIL hypercarry and Ratio/Jing second half\nDHIL brute force first halfAventurine needed to tank Boss Aventurine in second halfThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'ID'), 
    ('Yummy Hu Tao wig soup\nCosplayed her a long time ago and thought about cleaning the wig since it was pretty crusty\n\nAlso Mizuki cosplay pics possibly soon', 'EN', 'JP'), 
    ('Splash Arts\nJust splash arts of the three husbands + Trailblazer\n\nWhich Trailblazer do you guys use the most? Physical/Destruction or Fire/Preservation?', 'EN', 'RU'), 
    ('What made you want to play Kafka in game?\nHer appearance and personalty definitely stood out to me when I first started the game. Plus her Ultimate looked really cool to me, and honestly stuck with me the whole game. I guess thats why I still main Kafka. What about you guys, what made you pull or choose to play her?', 'EN', 'EN'), 
    ('Finally i Got Kazuha 😭\nGuy s comment , how many do you have primogem💧\n\n1. Guy s Follow for Next next Redeem Code \n\n2. Go and check YouTube channel \n\n3. New started New channel channel', 'EN', 'DE'), 
    ('everyone know 🤭\ninspire by arlecchino animation', 'EN', 'CHS'), 
    ('Literally being an aesthetic collage maker ✨✨✨✨\nI WAS BORED- anyway, do you like them? I don’t know what I did. I just made them. That’s it, nothing special :)\n\nI might actually do more of these\nIt was pretty fun honestly\nSooooo feel free to comment which characters you want me to make a small collage of! It can either be Genshin or HSR! Any character of your choice! (Might do four or five comments each post)', 'EN', 'JP'), 
    ('arlecchino 🙏\nso so so excited for her to come out, I can’t waitttt 💪 im so happy on how this drawing turned out, I managed to draw a decent side profile! bro she is so fun to drawww, especially her hair lol. don’t question why there’s no eye.. I got lazy.. 😰\n\nanyways, any time I listen to the song “little dark age” it just reminds me of arlecchino, idk why 😭👍 I kinda wanted to make a short animation using the song, but then I realized it would take me too long and I would probably forget to finish it 😔 one day im gonna get better at animating ‼️\n\n4.6 needs to come faster fr 🙏🙏', 'EN', 'VI'), 
    ("100% in Monstad! Finally! Now on to Liyue!\n#liyue #monstad #100% #finally #atlast You have no idea how long it took me to finally get this in Monstad! I'm proud of me!", 'EN', 'JP'), 
    ("Help with Co-Op teapot \nPlease help me to get this last achievement for level 3I'm ar56 NA server, and all my friends have stopped playing. You can take anything from my world if you need it.", 'EN', 'EN'), 
    ('Sketch a Day #253\nI did not expect to adore Kakavasha and Aventurine as much as I do now. 🥺 \n\nNow if only I have enough resources to guarantee his pull... \U0001fae0', 'EN', 'TH'), 
    ('Sparkle high pitch sound ult\nSeems only me noticing it and it wasn t there before a month ago I had to compare it from the other videos from YouTube\nisn t present in those videos. I just hope to get fixed soon it gives me a headache after few fights ', 'EN', 'CHS'), 
    ('NAME RESEARCH parte 4: ❄️LA SIGNORA🔥\nLa Signora (pronounced [la siɲˈɲoːra]; lit.\u2009\'the Lady\') is a character in commedia dell\'arte. She is the wife of Kuba and the mistress of Alexas. She is tough, beautiful and calculating, and wears very wide dresses along with very heavy makeup. She walks with a flick of the toe and her arms held far out to the sides of her body.La Signora could be a "courtesan" (high-class **********), but typically manages to wrangle her way into the household of an old man, usually Pantalone, where she would inevitably ***kold him. She was an older, ******** experienced Colombina, known as Rosaura.(Information comes from Wikipedia)', 'EN', 'VI'), 
    ('this animation was actually so cool omg\narlechinnos backstory is so sad', 'EN', 'JP'), 
    ('Day 3\nDay 3 of posting for jingliu frame~', 'EN', 'JP'), 
    ("Zuo Ran came home again \U0001fa77\U0001fa77\U0001fa77\nFrom 90 pulls to 51 pullsSo ready if i got it on last pityBut then after seeing the probability listDecided to gave it another one pull and bam rainbow ✨✨✨Thanks for coming home again Artem 😭. After i got a bit lucky in the 1st anniv rerun,didn't expect to get lucky again and was expecting hard pity. But then,he came back.🥺🥺🥺", 'EN', 'VI'), 
    ('What’s Wriothesley’s favorite tea flavor?\nThis is not a joke. I suppose it’s black tea, since it’s like the standard kind. I’m not sure if I missed him saying otherwise ', 'EN', 'RU'), 
    ('and finally i did it!!!\nabyss 36 star after 1 year try...', 'EN', 'DE'), 
    ('I m not ready to level up I like being lol 69\nI need to stay level 69 don t level me up :(', 'EN', 'VI'), 
    ("Acheron had a terrible build but I just about managed\nWon't lie, my Dan Heng team definitely carried this floor. 3 cycles side 1, 7 cycles side 2. Probably should have used a different DPS since my Acheron is lacking in a good LC but I wanted to try her out. I was using a level 80 Himeko LC (because of the high base atk). One thing to note is that adjusted my sparkle spd to 173 so that the 12% spd debuff wouldn't be too effective. Aventurine's placement is also pretty important so that I could get my ultis up quicker from the energy gained from getting hit. It felt a lot harder than the previous MoCs, definitely.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'CHT'), 
    ('New blade build\nStill need to change my planar to the other set but been farming for other people. Decided to go for two piece instead of the set because kept ending up with 120 crit rate. Plus will max his weapon eventually so will get to base 70 crit rate on his next rerun.', 'EN', 'RU'), 
    ('all in\n30 pity, blessed by aventurine’s luck', 'EN', 'DE'), 
    ('Ship tier list!\nI m not really a shipper but I wanted to rate some ships...please if you have an opinion feel free to speak it!...I feel that there will be some hate for where I ve placed some of these ships so I apologize if any of your ships are placed in the definitely not section or the not my thing section also this took awhile but I m glad I got it finished!', 'EN', 'ID'), 
    ("Wanna give a shoutout to my HSR friend\nThank you for your e6 Acheron, without using her as a support, I don't think I'd be able to get Aventurine's trace materials so fast.", 'EN', 'RU'), 
    ("My luck is shining a bit too much this patch... 😃\nI didn't had any hopes of getting any 5* weapon early... Well at least something is better than nothingI was trying to get neuvi's weapon but ended with kazuha's XD", 'EN', 'JP'), 
    ('Argenti is truly a knight of beauty\nGU1K4CRA6N (My code for the share your code event lol cos I completely forgot about it then remembered im f2p i need it lmao) Anyway just did argenti’s quest and i lowkey see him in a more beautiful light, still weird for rizzing a plant, but he’s still a good guy', 'EN', 'FR'), 
    ('Cyno!\nneeded something to doodle and Cyno volunteered!', 'EN', 'VI'), 
    ("Me everytime I need to choose the sacrifice\nDon't worry, Acheron and Black Swan to the rescue", 'EN', 'VI'), 
    ('….what???? 100 follows???? 😭\nYOOO WHAT?????????? How did I get 100 of you lovely people to follow me 😭😭😭😭😭\n\n\nI never thought that I’d get to this point or even get any attention at all, so thank you guys sosososo much <3333 I say this a lot, but I really do appreciate all of you guys’ love and support!!! It means a LOT to me that my art, cosplays, and covers actually are enjoyed 😭😭😭\n\n\nIn honor of this milestone (this seems pretty big to me, idk) how about I host a Q&A? Rules are no questions about personal information (like about my age, etc)😁\n\nAsk your questions down below, if you have any!!', 'EN', 'ID'), 
    ('Well you accomplish your goal phoenix_c\nTysm for all the likes it means a lot to me♡', 'EN', 'KR'), 
    ('me when arlecchino gets released\ngrinded all month for her lmao', 'EN', 'TH'), 
    ('Mageblade corrouge\nJust spent 30 minutes of my time swimming and dodging the bubble, than attacking mageblade with XENOCHROMATIC JELLYFISH and defeated it\U0001f979😨Then googled it just to know you need to use the XENOCHROMATIC BALL OCTOPUS to defeated it faster 🥲🥲🥲', 'EN', 'CHS'), 
    ('Auto team\nF2p player...Barely 20 cycles left...The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'FR'), 
    ("Day 6 - Cool Pose\nY'all should try to take ei's photo using 2nd acc to explore more pose. A lot of nice shots with new angle we can get. This is one of the example ", 'EN', 'RU'), 
    ("The Knave is calling me!\nI'm sitting on my pity waiting for the father to release. Two more days just but it feels like eternity.Knave : I'm surprised you want me so much. Me: you don't know how much. Knave: bless you. Finally i shall see this image after my wish right after the update. I'm pulling her! I will there is a clock in RL, I can't wait two days.😭", 'EN', 'TH'), 
    ('Was casually gliding then this lil guy decided to be silly\nI literally glided by thinking “wut da fook?”', 'EN', 'JP'), 
    ("MOC 2.1\n1st team only needs 2 cycle to clear but the 2nd team....  It's not jingliu is bad but aventurine boss is so tanky ugh..", 'EN', 'VI'), 
    ("So who else is in the beta?\nI see a lot of people complaining they didn't get into the beta and that's a very valid complaint, but I want to talk to the players that got in.How are you vibing with the game? Having fun? What S rank did you get from Stable Channel?I'm having loads of fun, this game is just beautiful and the gameplay flows beautifully even if it took me the whole prologue to understand what the hell is Daze.As for my luck, it might be as bad as always but I somehow managed to pull this man, so I'll be a happy creature for a while:I mean, steampunk wolf that kicks enemies very hard. I might be turned into a furry by his existence alone.", 'EN', 'DE'), 
    ('i need some help yall 💀\nso im currently debating on if i should wish for neuvillette or if i should keep saving for arlecchino since i have basically farmed almost everything i can currently for her but i feel like neuvillette would make my account better. i dont mind just saving for arlecchino’s next rerun either. i dont know what i should do honestly so what do yall think?', 'EN', 'TH'), 
    ('ITTO ITTO ITTO\nStolen Itto memes tee hee <3', 'EN', 'CHT'), 
    ('THIS SHĪT AINT FAIR\nWHY IS ARLECCHINO PLAYABLE BUT NOT DOTTORE?!AND ALSO SIGNORA BTW IDC IF SHE DIED TINGYUN DIED IN HSR BUT SHES PLAYABLE BRO DEAD PPL IN HSR BECOME PLAYABLE SO WHAT ABT GENSHIN?! WHY IS HOYO GIVING HSR PLAYERS SPECIAL TREATMENT?!AND STOP BEING LIKE "arlecchino is the best fatui harbinger!" ITS ANNOYING SHES OVERRATED AND YAE MIKO AND JEAN ARE HOTTER THEN HER SO PLS GENSHIN MAKE DOTTORE AND SIGNORA PLAYABLE ', 'EN', 'EN'), 
    ('Kaeya, the new elsa\nif you re girl has long hair\nmysterious eyes and an eye patch \nwears clothes with boob space\n\nthen that s not your girl, that s our Kaeya bbg', 'EN', 'FR'), 
    ('(26 screenshotted) I try to kill my friend but…\n*soak self in water anyway**thinking about something evil*yes yes few hp instant killyes yes yesno no no..damn the food whyno no no..', 'EN', 'FR'), 
    ('Silver wolf day 14\nWhat rank would silverwolf be in valorant?', 'EN', 'RU'), 
    ('130 pulls just for him\nI started saving after I got Argenti', 'EN', 'FR'), 
    ('Team Comp for new f2p\nHello!!! I was wondering if some more knowledgeable HSR players could recommend a team comp with the characters I own.', 'EN', 'CHS'), 
    ("Is this good?\nHi i need help with somethingI recently got neuvillette and i want to know if my build is ok or notDo i need more CR or it's enough?I'm still farming for the talents material and i got this far for now I will level up the weapon in future i just wanna know if this one is good or notThank you for helping", 'EN', 'ID'), 
    ('in your opinion…\nis it worth it to go pull neuvillette if you have ayato? I actually love playing ayato but neuvi trial was rly fun. im f2p btw. and im prepared to 100% my map for arlecchino. so idk cuz neuvi is fun but I LOVE arlecchino’s design. and idk if neuvi is worth it for my account if im planning to get arlecchino and already have ayato', 'EN', 'RU'), 
    ('Best girl Chiori\nRead title (Navia best girl too ofc)', 'EN', 'DE'), 
    ('How my 2.1 Pulls went!\nI’m actually so happy I got Aventurine, I fell in love him with the MOMENT I heard his voice from that one call with topaz. While I am kinda pisse* that I STILL don’t have Lighting dps but Oh well ig. But still I’m happy that Aventurine is home so I can give him the love he deserves.', 'EN', 'RU'), 
    ('Dr Ratio\nGuys I want himIm such a narcissist that I just find it hot at this pointThat one lightcone with the gun… OMG Kiterally drooling like ', 'EN', 'KR'), 
    ('Best reporter and photographer ever\nCharlotte has to be the best reporter and photographer of the steambird so far cuz no one can get a scoop like Charlotte', 'EN', 'JP'), 
    ('Tighnari fanart :3\nHeyyy, I tried water colour for the first time a few weeks ago and this is one of the two works I did, I hope you guys like them :3', 'EN', 'ID'), 
    ('day 1!\ndidnt know there was companionship for aven tooo', 'EN', 'CHS'), 
    ('Neuvillette s Signature Weapon\nI got Neuvillette s signature weapon. The last time I pulled from the weapon banner was when I got Furina s signature weapon. Is this luck?', 'EN', 'VI'), 
    ('do you ever love one man so much\nMostly free to play but I had to go all out for aven... here s to hoping Robin comes home early because he did not make it easy 🤣', 'EN', 'JP'), 
    ('Amplifying Test\nJust to have an additional draw to win nothing lol', 'EN', 'VI'), 
    ('Saving for wanderer - Day 11\ntoday was my first day off so im thankful to say i entered S E R I O U S    F A R M I N G   M O D E\n\nprimary methods were exploration (today: serai island) and story quests (today: childe s and chiori s)\n\ni realized i had two acquaint fates and wished for funsies and i accidentally got sucrose. whoopsie\n\njust with the things in my bag and like 80 resin i got her to lvl 70, gave her my nahida s lvl 80 mappa mare and got it to 90, put on my viridescent set i saved for kazuha (but retired cuz imma skip him lololol) and got her to 590EM and 150ER \n\naccidental win for me', 'EN', 'CHT'), 
    ('Voice line\nWhich Nahida voicelines are your favorite? ', 'EN', 'CHT'), 
    ('Best team\nCause i dont have jing liu. SadgeThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'CHS'), 
    ('I need help for a hyperbloom team\nI felt like, since I got Neuvilette recently, I should make a team of him.\nI watched a couple videos, built him a little, but what team should I give him.\nBefore, I tried running a hyperbloom team with a bunch of four stars and a Mona, which wasn’t too good, but now I have Neuvilette.\nI have a Kaveh and Kuki, which is fine.\nBut I don’t know whether I should put Faruzan or Lynnette on my team for swirl, can someone say which is better for a Hyperbloom team with Kaveh, Kuki, and Neuvilette hyperbloom team, Faruzan or Lynnette?', 'EN', 'KR'), 
    ('Co-op\nI had a encounter with an inappropriate player in co-op mode. So I am just chilling in inazuma doing quests and I get this co op request, I accept it, because I am nice. This person was SOOO inappropriate, they were acting like a friend but then things started getting weird. Like in the chat they would ask weird thing like when I was farming for one of my characters they asked if they could do "things" with me. I asked what they meant and they said, "i mean do that with you". I kicked them out and reported them. So yeah. BYEEEEE ', 'EN', 'JP'), 
    ("Alt Account\nSo, I was thinking whether I should Visit my Alt account a little bit and mess around cuz I'm bored.  But I realized, I had to logged out first. Which I'll never do! It would be a pain in the b*tt if Logging back had an Error again, like typing the password but it says incorrect.Dont wanna switch pw again.", 'EN', 'FR'), 
    ("Daily Clara post\nLike if you like Clara, comment why if you don't ", 'EN', 'CHS'), 
    ('Happy Birthday Yelan!💦🛐\nOne Of The Best Hydro Characters💫\U0001f979\n\nShe s so good that I wish I had her, but I m saving for someone else(right now)😭', 'EN', 'RU'), 
    ('Dori\nDid anyone ever notice that Dori wares overalls  ', 'EN', 'CHS'), 
    ('Konage’s look before she died \nShe was like this just before she died, (she snuck up to the school roof to check on a plant she was growing in secret on the roof and then she got pushed off) I tried to go for the 2000s look since she died around 2002 and her bangs are a bit different since she got her eye stabbed as she fell so she styled her bangs to hide it', 'EN', 'FR'), 
    ('A walk would be nice, but.. it rains?\nFeaturing Lady Furina and Sigewinne as students.They walked home together after the school bell rang.A few steps later, rain started to pour.Sigewinne: "Luckily I was ready with my raincoat the moment we stepped out of the school\'s gate."Furina: " A luck too when Neuvilette passed me the umbrella this morning. Like he already knew it gonna be raining."Sigewinne: "Oh, what he is doing at home?"Furina: " Not so sure. But when I left this morning, I saw he was ready to watch movies on TV."Sigewinne: "Ops..- don\'t tell me they are sad movies."Furina: "Huh?"ops- it rainsafter the rainprogress', 'EN', 'RU'), 
    ('hear me out\nHu Tao is the greatest character known to mankind because of her great personality and bcuz I said so and also because she is honestly best liyue character ok? The reason why I like Hu Tao:\nbecause I love ghost girl with brown hair and bc I’m not mentally stable and she gives me life', 'EN', 'CHS'), 
    ('I need answers.....\nI get why people say she is like spider.. i can see it here. . . But then. . . Someone explain me why she have wing.  (As far i know spiders do not have wings.)( And i think i know why ONLY one wing. .. coz it is easier to play. Two wings would be too complicated - i Guess - and blok to see her desing , while exploring or in combat.)And here she looks like incarnation of pyro crystal fly.   What should i make of this?', 'EN', 'KR'), 
    ('This is really sad\nIf you are going to call me a homophobe and trash talk me, at least have the courage to keep the comment up instead of just deleting it to avoid it. (Copium Yae by Naedix)', 'EN', 'EN'), 
    ('Aventurine Banner Submission\nIf Aventurine would be best described by any card, it would be this one. He’s so unpredictable, buddy seems like the type to randomly slam a uno reverse on the table.', 'EN', 'JP'), 
    ('[Version 4.5] - F2P Neuvillette Hypercarry & Nahida Hyperbloom\nI recorded a video of the perfect run I shared below, but with a slightly different Furina build as I got her a hydro goblet today.\n\nEven with my WIP build, Neuvillette is a powerful hypercarry… the supports did a great job buffing his damage!\n\nI can’t connect my PS4 controllers to iPad at home without accidentally turning on the PS4, so in the end I did this with my Backbone controller and my iPhone 14.\n\nThis is the second time I’ve ever played using the Backbone so please ignore the rotational mistakes especially the struggles on the second half of chamber 3. Sometimes I simply forgot what button did what as it’s a little different from PS4, and first time plunging on this controller! ', 'EN', 'VI'), 
    ('Boothill and Robin’s song\nOk I don’t particularly ship them but if they were to sing a song together I can’t help but imagine them singing Meant to Be by Bebe Rexha and Florida Georgia Line. I seriously cannot get it out of my head.', 'EN', 'ID'), 
    ('Week 4 of Pick Up Lines in BottleMi\nUh oh. Albedo, get your sister! \n\n(Sorry it’s late, got busy this week! 😓)\n\nRemember, if you have any suggestions for pick up lines, let me know!', 'EN', 'TH'), 
    ('i have my aventurine with broken keel set but the 10% crit damage is no where to be found the effect resist is too high for the broken keel not to activate\ni think the broken keel is broken pls fix it', 'EN', 'KR'), 
    ('Got Adventurine!!\nI haven’t done Penacony but all the spoilers I see about him made me want him more (aside from his looks and being Preservation and Imaginary). I lost 50/50 to Clara so I had to go All or Nothing and used up all my jades for him. I would’ve wanted his lightcone too buuuuut… no more jades ', 'EN', 'RU'), 
    ("Question: Combat functionality or characterization? How do you choose your companions?\nTa-da! Hey, everyone! I'm the exclusive Penacony-limited Chat Trashcan!Trailblazers would summon various friends to Trailblaze with them as they travel in the cosmos~How do you select your companions?The topic this time is:How do you select your companions?Ding-Dong! Come and join the big trashcan family!Trashie FamilyRemember to change your server username into your HoYoLAB ID after you join the group~!", 'EN', 'KR'), 
    ('Archeron / Jing Liu teams.\nTesting sparkle with jingliu and aventurine with acheron. Both work decent enough!The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'KR'), 
    ('Daily rant about dr ratio mischaracterization :3\n"hes racist"pls, plsplspls read the dialogue, he stated that aventurine was a slave to the IPC, as well as being from sigonia !!! he was stating a fact ( that aventurine is sigonian ) , something other characters have done, unlike sparkle who has actually insulted the sigonian RACE and not just aventurine !! :3', 'EN', 'DE'), 
    ('acheron daily post !!! :3\nacheron is crazy LIEK HJOW THE FLIP DO YOU LIEKE SOEUUDJWJ one slash of her sword like shes INSANE i loev her so mcuh', 'EN', 'FR'), 
    ('No Acheron. Gepard is still good.\nRuan Mei keeps the dino broken. Gepard spams ult thanks to having over 134 speed with energy regeneration rope. Finished first half within 3 cycles. Second half is hard with Jingliu and the Aventurine boss ability. Luocha is very good at keeping the team alive. Pela barely survived. Got it at the very last cycle.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'CHS'), 
    ('3rd 50/50 won in a row! (:\nThank you Aventurine for coming homeee. 😩🍾', 'EN', 'CHS'), 
    ("Explore and Gather\nI just want to post pictures of that time I explored the Vourukasha Oasis for the first time.Usually everytime there's a new area dropped I do the world quest first and not touching any puzzle or challenge until i have the time or necessary for me to gather primos. I reread quests and books sometimes bcs I tend to forget things and idk.. I like knowing lore.I had a lot of fun in this area. The fact that they dropped a hug lore related to khaenri'ah was such a chef kiss. I just know the upcoming Remuria related new area in 4.6 will blow me away just like Vourukasha Oasis did.I remembered one of the quest here related to Narcissenkreuz, which talked about Reneé and what they were doing in Sumeru. Even though at the time it was a huge question mark for me.I hope there will be a new world quest relating to Natlan soon. I need it! I need loooooorrreee.Before and after I explored while finishing the world quests. Alhaitham's skill truly a lifesaver when I explored this area. Never been so grateful for him on my account.", 'EN', 'RU'), 
    ("Wholesome\nWholesome HoYoLab doesn't exist it WILL hurt youWholesome HoYoLab:..........It doesn't exist guys!!!!!! ☹️☹️☹️😭😭😭😭😭😭😭😭😭😭😭", 'EN', 'TH'), 
    ('SPRINKLES X HSR - March 7th Cupcakes! 💖🧁\nI wanted to share my small journey to get these cupcakes! 🧁 \n\nTHE CODE CARDS LOOK SO CUTE! 🥰 \nTHE CUPCAKES ARE SO CUTE! 🤩\n\nI actually took off the March 7th sugar deco and froze them ❄️❄️\n\nI’m keeping them FOREVER ❄️❄️\n\nStay tuned for the HSR cupcakes coming out next week! 😎😎\n\n- oli ✨', 'EN', 'RU'), 
    ('Favourite dps?\nComment your favourite dps and the reason why', 'EN', 'CHS'), 
    ('Everytime\nMe and my other friends just watched', 'EN', 'TH'), 
    ("Can t wait....but I also need time..\nI'm absolutely so excited for Boothill! Like rlly badly. But I don't have that much crap for him so I've been grinding-ish. But that is all I hope y'all have an amazing day / night!♡", 'EN', 'CHS'), 
    ('Deja Vu!\nXaoi , Zhongli , traveler , Paimon', 'EN', 'JP'), 
    ('Anemo slime\nI’m going to make a different slime each day', 'EN', 'JP'), 
    ('Person closest to Wriothesley\nSigewinne. And that chick of whom i do not remember the name of. *facepalm*And then Neuvillette, i want to imagine. *shrugs*', 'EN', 'KR'), 
    ('My  regret  Pulling for list!\nPlease note that I do not have any regrets about pulling on characters, and like all the characters (other than Qiqi and Dehya)\n\nThere are definitely some characters I like more/use more, but I have pretty much used all the characters consistently at some point (other than the standard banner). Also, please note that the characters that I don t have/don t want are just characters whose playstyles I don t like very much/don t see myself using all that much/don t like the personality all too much! I mainly pull depending on whether I like the character, which is why some characters have no cons versus those with multiple!', 'EN', 'VI'), 
    ('Well that s interesting\nI found this card where Gallehger was sitting. it wound up being a sticker for  Maeven Ellis, a halovian singer. at least I think she s a singer based on the name of the sticker. It makes me wonder if there are any other small designs for the pick-up-able stickers or other reading materials I might have missed.', 'EN', 'ID'), 
    ('Tag arlechino , in comments to get to witness her AI\nTag your options for other characters too', 'EN', 'KR'), 
    ('F2P line up for those who don t have answer on 1st phase \nThis stage really test your strategy , no sig on support ex swThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'VI'), 
    ("the same team again lol\nthis time it's not autobattle bcs ai goes for the small  shrimps firstThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'CHS'), 
    ('Arche\nA genshin oc I made a while ago.', 'EN', 'DE'), 
    ('I just started Tears of Themis…\nI only started the game due to wanting a story with mystery. And honestly I find the Mc to be more attractive than the guys. ALSO SHE KNOWS HER CLASSICAL MUSIC!! That’s honestly enough for her to be my favorite. She’s also beautiful!!', 'EN', 'JP'), 
    ('WIP update 2\nI went cross-eyed 20 minutes before stopping, I m so tired but so happy to see her coming to life.\n\nSorry all my pics are so pixelated, I have no clue how to do screenshots on a tablet lollll', 'EN', 'RU'), 
    ("Hello everyone! I m new to the game it looks cool thats why i tried to play and the story is so cool too so can you help me with somethings?\nHello i got the blue guy from wishing he is a 5 star whos name i cant remember i am going to inazuma cause im done with liyue. May i ask on how to level him up i only got him level to 40 because he have a free level up materials from the trial i got him from the wish when i wish like 30 wish it turns gold and i got him. The only problem is my traveler is at level 60 while this guy is at level 40 🥲 i can't find his materials i look everywhere but can't find it.Btw his so strong he shots a tons of water! He is so cool and he drinks water allot if i don't move hahahaha and also make rain stop🥲 i mean something in reverse he also deals like 1k even at level 40 the only problem i got from him is his life drains when i do the hold attack and i cant control it so he kinda sucks🥲", 'EN', 'DE'), 
    ("Why do i like march?\nShe starter to grow on me once i realized that she wouldn't leave us for a long shot. To be honest i just became fond of her, even when she's more energized than me", 'EN', 'ID'), 
    ('look at this stupid ass- 😭😭\nmanga : To Make A Delicious Omega Squeak', 'EN', 'JP'), 
    ('Happy birthday Yelan!!\nIt’s the QUEEN’s bday so lemme show y’all mine’s highest dmg bc why not this was during version 3.6 so long time ago🥺 I got Yelan during her first banner, 2.7. I first planned on skipping her to get kazuha but in the end I couldn’t resist she looked iconic and in the end I won both her and kazuha’s 50/50 and later got her weapon during sumeru so THANK UOU MY ICON FOR CARRYING ME MY WHOLE GENSHIN JOURNEY 🥰😍🥺 All you Yelan havers don’t be shy show my what ur highest dmg youve ever done on Yelan :3', 'EN', 'EN'), 
    ('CODES for April updated\nHere are all of the new Honkai Star Rail codes:5AJTZPPMN8VB\xa0– 100 stellar jade\xa0(new!)QBJTY77MN9T7\xa0– 20k credits\xa0(new!)CHARMEDONE\xa0– four adventure logs (new!)ALLORNOTHING\xa0–\xa0one all or nothing and 10k credits (new!)LUCKYGAME\xa0– three condensed aether (new!)BTKBH6P47B77\xa0– 50 stellar jade and 10k credits (new!)0327CARNIVAL\xa0– two sour dreams soft candy and 5k creditsHSR1YEAR\xa0– one all or nothing and 5k creditsMOREPEACH\xa0–\xa0three traveler’s guides and two sour dreams soft candyST3SHPNLNTN3\xa0–\xa050 stellar jade and 10k creditsSTARRAILGIFT\xa0– 50 stellar jade, 10k credits, two traveler’s guides, and five bottled soda', 'EN', 'TH'), 
    ('Sunday s name in Chinese\nI just realized Sunday\'s name in Chinese is 星期日 instead of 星期天 (what my region also calls Sunday in Chinese).Still, I think I\'m going to unofficially call him 星期天 so I can give him the nickname 我的天 (literally "my sky", but actually means OMG) ', 'EN', 'RU'), 
    ('Aventurine Banner!\nI love Aventurine!It was very luck that his banner started after the anniversary and it was very nice that the anniversary rewards were so good!Thank you Honkai Star Rail team!Were you able to pull him? Do you love him as much as I do? No matter the answer I wish you luck!', 'EN', 'CHT'), 
    ("Almost maxed out Misha traces\nRan out of credits but only have 3 more trace upgrades to do. I think he's going to be my first maxed out char he's fun", 'EN', 'DE'), 
    ('unrelated but❗️❗️ (in desc)\nanyways so i was watching kabe koji bc bored & i had dropped it a while back, AND TELL ME WHY ON THE SECOND EPISODE I GOT JUMPSCARED BY THE BLONDE ONES SOUTH CAROLINA SHIRT… like ik it’s literally only me freaking out but now i have to pause and laugh every time his shirt is visible just bc like ‘oh haha my state wow yippee!!’.. like do they just sell random ahh English shirts over there without knowing what they say❓❓❓ like oh mm a shirt in english NICE❗️ wonder what it says.. South Carolina?? tfs that\nanyways food for thought ig❗️❗️ and slightly doxxing myself but whatevs', 'EN', 'DE'), 
    (':3\nGive me silly wisher challenges', 'EN', 'CHS'), 
    ('C0 Xiao Double Electro + C6 Pyro Xinyan Vape [4.5 Spiral Abyss | Floor 12]\nHoly. This Xinyan team with this Crimson set against that Enhancer Mek is nuts. I really want a nice EM sands for Shimenawa now (or an Att sands, that d would be nice too). This Crimson set also needs wayyy more Att stats. Though the on set pyro gob and circlet is nice that I got somewhat recently. Since my Shimenawa set uses a DEF sands, its only good for her charged att pyro teams. I ll do a short video with Xinyans team against the Mek Local Legend next.\n\nAlso, for Xiao, I m surprised I had energy issues. I was going for a burst spam team but I guess the electro resonance but isn t enough. I might have a VV piece that has more ER to give to Faru but Idk if that ll help Xiaos burst regen. ', 'EN', 'CHS'), 
    ('LUCKIEST HUMAN COMMENT HERE PLS\nShow ur luckiest luck here!I wanna get jealous \U0001faf6', 'EN', 'FR'), 
    ('Jingliu come home\nDay 3 saving to finally get you', 'EN', 'CHS'), 
    ('Just realized\nMan I just realized I can command their emotions and pose! Once again, doing this till I get that good Acheron stuff.Acheron saysPhoto editor used to add text and speech bubbles= (AI photo editor)PS the red is reference to her conversation vs. her Real words.', 'EN', 'TH'), 
    ('Non-Hoyo OC stuff + DTIYS announcement!\n(Probably won t post abt them here again, just using them as an excuse to make a filler post. But feel free to check out my twt (@ sleepyotakuu) if you do wanna see more of them! :]) \n\nFriendly reminder that the deadline for the DTIYS event is the 23rd, which is fast approaching! Please try to have your submissions posted by 11:59 pm CDT  (GMT -05:00)! 💖\n\nAlso the fandoms for the ocs are ensemble stars and obey me respectively :3', 'EN', 'RU'), 
    ('arle plis come home\nill let you step on my face plis', 'EN', 'JP'), 
    ('Coconut mommy\nI was hesitant to pull but her story quest made me to pull.I am always pre planned what I need for my team but she is only exception her personality made a impression on me.', 'EN', 'JP'), 
    ('📍 Sumeru : Vissudha Field & The Chasm 🪤 2 Precious Chests ✨️\n1. Sumeru - Vissudha Field\n\nIts on the most upper top area of sumeru, just go to the exact location and you will find a locked precious there. Dont worry, its easy ~ just beat the whole group of Fatui that exist there, and take the reward \n\n2. The Chasm \n\nGo to the blue arrow location. The closest and easiest way is to teleport to the domain and climb up all the way there .Bring your best anemo cuties ♡ \n\nAnd just hit the 2 stone as mr. Rizzlee did on the picture, and voilaaaa enjoy your chest ~ \n\n♡\\\\(=^•x•^=)/♡', 'EN', 'CHS'), 
    ('TWO JINGS STRIKE AGAIN!\n5 cycles used• All 5* characters used are E0 & are using alternative light cones• E6 Pela & E4 Tingyun• F2P with OK/decent character stats*May or may not work for you as overall build, stats, playstyles, & other factors vary among players :)The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'DE'), 
    ('Now I have to save up for Robin and Boothill AHHHHHHHHHH\nI just want to go insane...Why do they keep releasing great and hot characters? I might have to spend money on the game ', 'EN', 'FR'), 
    ('Too sweet cats\nTattoo game will be to much sweet to play 😂👌', 'EN', 'FR'), 
    ('GUYS 😭 I need 5* recs!!\nHey guys!! I’m back I’m 110% pulling for Wriothesley and his C1 and everything when he comes back, but after that.. where to?? My only 5* (that isn’t the Traveler) is Tighnari, and he’s completely benched So who should I pull for after I start maining him??I know Kazuha is kind of off the table since he’s currently running and that Shenhe and Kokomi probably won’t be on their respective chronicled banners, but other than that, who would be good for a Wriothesley freeze/melt/hyperfridge team??Im still quite new to Genshin so any tips would be appreciated ', 'EN', 'DE'), 
    ('These next 3 days are going to be torture\nI need arlecchino now, got a guaranteed and 55 pity. In a perfect world, I can get arle from a single ten pull and then her weapon within the 20 days that banner is up. BUT I do already have lyneys bow so idk if it s worth it BUT scythes are cool 🗿. Good luck to anyone summoning for lyney or arlecchino \U0001fae1', 'EN', 'DE'), 
    ('F2P luck\nBow again?! 🤨 oh wait what is that??? 🤩 My first 2 fivestars in one pull ever and 0 pity😮 what is that?!? I spent about 170 puls on Riden weapon… my Kazuha is so lucky even C2 about year ago was like in 50 pulls.\n\nHave you ever pulled 2 fivestars in 10 pulls?', 'EN', 'CHS'), 
    ("Kuru kuru & Nuk3 \nFirst half is Herta hyper carry just let her kuru kuru.Second half use Acheron's ulti at the start of any of your characters (this will let you be the first move on the next wave). Enemies will help  a lot charging your ulti so be careful with the extra charges. I tried to make it with auto battle, but I think the game hates me, cuz I got like 2k per half, maybe you get better scores than me. Also I have low investment characters, and you can use Pela instead of Guinaifen (I don't have Luka's LC)The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'DE'), 
    ('Fontaine, Fortress of Meropide, Piltover and Zaun\nguys are Court of Fontaine and Fortress of Meropide design inspired from Piltover and Zaun from league of legends?', 'EN', 'FR'), 
    ('Week 3 Saving for Venti Cons\n45 wishes! 9 pity, 50/50\n\nwith two more wishes in reserve with stardust(? glitter? i mix them up lol)\n\nanyway, the goal is to get C2 at least, preferably C6 (which I should be able to get, right? 5.0 is a couple patches away and i doubt they re going to rerun him first lol)\n\ni have a habit of losing every 50/50 i want to win, and winning the 50/50s i want to lose (lost Kazuha and Alhaitham s 50/50 on the same banner, lost Kokomi s 50/50, won Childe and Neuvillette s 50/50 back to back bc i wanted starglitter, lost Venti s 50/50, lost Baizhu and Ayato s 50/50s and won Xiao s 50/50 when I was, once again, pulling for starglitter lol) anyway, the standard 5 wishes every month should keep me relatively topped up so i hopefully don t have to risk that between here and now lol', 'EN', 'FR'), 
    ('Light and Shadow\nSometimes, a silhouette is all you need.', 'EN', 'VI'), 
    ('Kazuha Cosplay🍂🍁\nI cosplayed him at the AniMinneapolis convention ;)', 'EN', 'CHS'), 
    ("Hello, I m back!\nHello people, I haven't posted a long time causr I deleted HoYoLab, since it was useless (I thought so) because l deleted Genshin Impact (I thought that I didn't have enough room for it on my phone). But if you're reading this, then all my thoughts were WRONG cause I'm STUPID, and I'm back. Yeah that's it.", 'EN', 'JP'), 
    ('SleepyOtaku s dtiys\nI can t shade for life😔\n I originally started this when the dtiys was first announced but then I went on a roadtrip for a while and put off the drawing because I didn t wanna worry about it too much so now it s rushed :DD', 'EN', 'ID'), 
    ('First Time 3 star MoC 12 Auto Battle\nThank you my Blind Queen and Direction Challenged QueenThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'RU'), 
    ("4.6 Fatui Only!!\nLumine:why baizhu let's change that *Switch it* Lumine: there this is perfect!!!Pantalone:......Lumine: so perfect complete I rather says it's a Fatui Wishes ( This photo is not mine I just see on Facebook)", 'EN', 'ID'), 
    ('genshin ships per character, random~! Pt 17\ngenshin RANDOM ships for every character pt 17, Heizou, Collei, Tighnari!\n\nUpright hearts = ship it\nReverse = dont, prefer over other\n\nPart 18 will be Dori, Candace, Cyno, stay tuned!', 'EN', 'TH'), 
    ('New player looking for team suggestions!\nSince i’m new to the game (i’ve only been playing 2 days) does anyone have any team recs for me?  I’ve been running with the top 4 characters but i’m thinking having 2 of the same element is maybe holding me back?? Should i have 4 different so i’ve a better chance  weakening enemies?? Any tips and/or suggestions are appreciated! ', 'EN', 'VI'), 
    ('What I’m looking forward to\nVery excited to get herrrr (I have guaranteeeee)', 'EN', 'JP'), 
    ('7 Mysterious Core Fontaine\nMysterious Core is a Quest Item obtained from chests after completing 7 Pneumousia puzzles. They can be submitted to Henri to start the World Quest Still Mouthwatering!.\n\nJika kalian kurang paham kalian bisa cek full guidenya di channel youtube Sensei impact ,cek link di bio atau Dm admin untuk videonya.', 'EN', 'DE'), 
    ('Art Block :(\nHad art block the past couple of weeks so I tried doodling again for the first time in a while <3 \nI don’t think it turned out too bad but I hope to return to making Genshin/star rail art soon', 'EN', 'CHS'), 
    ('🧃Shigure Kira,Fu Hua FOV and Ai-chan icons🧃\n-Icons edited by me💞\n-If you need icons of a specific character i am here🌟\n-Official fan art and trailer from mihoyo/Honkai Impact᯾', 'EN', 'TH'), 
    ("STANDARD BANNER IS INSANE!!!\n3 five stars in a single 10 pull?!!!! Tbh I was so disappointed thinking I had gotten Clara's lightcone and then boom Another one and ANOTHER ONE  Let it rainnnnn Ps: yaaas Bronyaaaa ", 'EN', 'CHS'), 
    ('My Current Team❤️\n my current team Im super in love with luocha his healing is out of this world even at E0.so im curious Who are your favorite party member? Let me know below ', 'EN', 'TH'), 
    ("Blessed Avgin - Aventurine\nNote: It's been quite a while since I have uploaded, but I plan on releasing some more photos in the near future from both HSR and GI.  My take on Aventurine: I started off thinking of Aventurine as an okay character, but as his story developed, I started to like him much more, and now I am an avid Aventurine main. He also somehow made my luckiest banner pull with coming home at 75-ish pity (guarantee), then coming home again right after - literally back-to-back, Aventurine then the next pull Aventurine again. I've never had luck like that before and probably never will again, but now he is E1 and I am a very happy main.Aventurine wanters will be Aventurine havers!", 'EN', 'TH'), 
    ('Got him\nGot him in 4 single pulls and his cone and 2 pulls ', 'EN', 'CHS'), 
    ("Neuvi  tism\nI mean, he doesn't really understand human emotions and he infodumps about water.Also, I'm autistic myself, that's why I like to headcanon him as such too.LOOK AT THISBro is sensitive to the taste of water.His soup is almost all water, and it surely doesn't have much flavor either.This? Autistic to me.Thank you for coming to my TedTalk  ", 'EN', 'CHS'), 
    ("Happy 1st Birthday Star Rail!\nLink to event + fun coloring book page: Stellar Jade Reward — Let's Draw a Cake Together! Honkai: Star Rail First One-Year-Anniversary Event~  Happy anniversary! Eat cake and be happy ", 'EN', 'CHS'), 
    ('When you think you have cried enough about Aventurine, but then you read his 3rd character story 😭\nNo wonder he doesn t get close to anyone.\nHis luck really does seem tocome at the price of others. 😔\n Let our baby be happy please ! 😢', 'EN', 'FR'), 
    ("AH !  I   M SORRY\nFor clearing up one of my last posts, the bathtub one..!I found it online and wanted to post it here. I didn't know it was fake. Sorry if I spread mis info 😅 but at least I go almost 100 comments...  still, hope ya'll who wanted to be in that bathtub commoission an artist 🎨 💅 ", 'EN', 'ID'), 
    ('EEEEEEEEEE\nwhy did my eraser disappear the moment I didn t feel exhausted and wanted to start drawing????? \nalthough, doing it without an eraser made me draw even more faster, wth', 'EN', 'EN'), 
    ("Best F2P sword for Furina ?\nI'm Currently using Harbinger of Dawn on Furina for CRIT DMG & that occasional crit rate. Here's my current build, what do you think is best for her ? if it's worth it then i was thinking of that fontaine fishing sword but idk if current one is best for me as it provides good crit for the current build i have.i'll be using her mostly with either Neuvillette or Raiden in Spiral Abyss.Current Furina build with Harbinger of Dawn 🌊Harbinger of Dawn R5 Lvl 90should i fish for it's R5 ?idk if it's good if i want her in Raiden dps team", 'EN', 'JP'), 
    ("Another day for Neuvillette Post\nThis is Neuvillette's Constellation, I'm just wondering if the other Dragon Sovereigns are still alive and will be playable in the future. Will their constellations look like this too?", 'EN', 'KR'), 
    ('Thank you for a 100 followers!!! (Q&A)\nSorry for not posting often I got swamped with like 4 different projects at school but rn I have a breather. :’) THANK YOU FOR A 100 FOLLOWS. I did not think this would happen so soon, I just wanted to post some of my random art and have fun here. So this post is gonna be a Q&A commemorate this achievement!  Feel free to leave any question in the comments below :D but if it’s too personal I will give a vague answer cus internet safety ;-; also if you wanna leave a small drawing request here feel free love you guys, I hope that today was a good day for you <3', 'EN', 'CHT'), 
    ('Rainbowwww🌈\nI was going to ascend my Zhongli and wanted to find a nice place, I never knew there were rainbows in the game😭😭', 'EN', 'JP'), 
    ('New Redeem code\n5AJTZPPMN8VBBTKBH6P47B77Free 150 stellar jade👌', 'EN', 'VI'), 
    ('who was Acheron talking to here?\nI had assumed this was on her planet but that wouldn t make sense, because (I thought, at least) that everyone on Izumo had died?', 'EN', 'TH'), 
    ('so i just started building my gaming\ntook me several tries to clear 12th floor because i am still not used to his gameplay but is he always this strong omg  even with low crit ratio and low talent level ', 'EN', 'JP'), 
    ('Arlecchino banner ritual guide\nFollow the step and to win 50/50', 'EN', 'KR'), 
    ('FURINAA\nDon’t worry guys! She’s just overflowing with Hydro…\n\nInspired by silent film makeup and that Focalors design by phosfulate on insta', 'EN', 'RU'), 
    ('Black Swan but Darker\nImagine how terrifying it would be to have Black Swan as an enemy as an ordinary person, someone who is not only powerful but is capable of playing with your mind.', 'EN', 'CHS'), 
    ('this quest is actually so good\nneko is a cat (for anyone wondering)', 'EN', 'ID'), 
    ('AHH\nDoes anyone know artifacts for layla that are really good so her shield actually works because i can not build characters ', 'EN', 'VI'), 
    ('OTTO WHY\nAS A LUOCHA MAIN I AM OFFENDED', 'EN', 'ID'), 
    ('What are you most excited about in 4.6?\nPulling Wanderer! Yeah I know To Vets that are seem crazy when there\'s a brand new character with a brand new weapon type (at least that was supposed to the case wasn\'t it? Scythes were being introduced and Arlecchino would be the first Scythe user, or did that turn out B.S and her "Scythe" is basically like Chiori\'s "Dual Weilding" I got hyped about and is just an aesthetics illusion and she\'s just a spear user with a Scythe looking weapon?But yeah, to me Wanderer is just as new and fresh as Arlecchino and find his backstory story extremely interesting, he\'s kinda loke the traveller, the one other soul who doesn\'t belong in this world (I mean you *could* argue Albedo doesn\'t but I\'d disagree, and I mean Lumine\'s around SOMEWHERE where I am in the story but Aether seems to have pretty much forgotten he had a twin sister (Paimon is gonna play the classical Lucifer role of charming, Cherub faced innocent pulling strings in the dark, I betcha! Even her hairband is reminiscent of the \'falling star\' as Lucifer was cast down. Lucifer "Morningstar" - "Lightbringer" Or maybe it\'s my morning 90mg Methadone and Clonazepam talking ', 'EN', 'FR'), 
    ('Filler for companionship rewards\nEven that aside, shoutout to the guy that somewhat carried me early on in the game for DPS options, even at MoC. Planning to build him later to start the cycle again.', 'EN', 'EN'), 
    ('Filler post for companionship rewards\nI recall being early on and struggle to beat stages and Jing Yuan support character system helped me a lot. Cheers.', 'EN', 'JP'), 
    ('Version 2.1 pull chart\nSo how was your pull going? \nit s a really unlucky version for me since I always hit 80++ to get a 5-star 😭😭\n\nI will use daily scrap jades to pull one-by-one for Aventurine. If he s still not coming then \\ Farewell, Kakavasha!\\ ', 'EN', 'TH'), 
    ('im tired\nthis is sadly my best artifact :(', 'EN', 'CHT'), 
    ('Arrlecchino will come soon! Arlecchino will come soon!!\nI listened this short event woth headphones. I could hear those stairs cracking into my brain after they went throw my ears No one:Arlecchino: X_XThis mini-movie got me, not gonna lie! It hit me with the chills and tons of questions!', 'EN', 'RU'), 
    ("Funny/nice Bottle Mi responses\nPs I did ask for permission to use the responses!One a question I don't have a screenshot of is who is your fav Landau sibling and why?", 'EN', 'DE'), 
    ('Aventurine wearing the same outfit as npcs\nBro has the default worker outfit 🗣️🗣️', 'EN', 'CHT'), 
    ('Will Aventurine Come Home or Not?\nHhhHhhhhmmmmMmmmmm. I am about 60-ish pity, since I can t get Acheron in my main account, only her LC. If I lose, I ll pull for Robin/Boothill or the reruns (if the rerun is Huo Huo). Anyway feel free to friend me (ASIA).', 'EN', 'TH'), 
    ('FIRST TIME FULL MOC CLEAR \ns/o to my boy Brandidon for help 😎The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'TH'), 
    ("Rip and tear\nI should really build more characters so I don't use the same ones over and over...The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'RU'), 
    ('I like my cakes how I like my men-\n-Imaginary.\n\n\nHeh.\n\nCake attempt with references to three of my favourite Imaginary boyos! Pretty last minute because that s just how it goes sometimes. \n\nHappy 1st anniversary to HSR!', 'EN', 'CHS'), 
    ('Aven Companion Day 3\nRandom pic with chest\nTaken on: 17 Apr 2024', 'EN', 'TH'), 
    ('My Rosaria and Eula Build\nThese 2 and Yelan are my favorite characters but this Rosaria build has been a great with supporting both Eula and Yelan. This build allows for Rosaria to keep her ultimate active as much as possible which boost the team s crit rate. Additionally while paired with Eula or another cryo character, it applies constant cryo damage which boosts the crit rate further due to cryo resonance. On a good run, it is possible for me to clear Eula s artifact domain in as fast as 10 seconds, and Yelan s in 15 with these builds.', 'EN', 'JP'), 
    ('Who to pull based the character I have\nGuys that all the characters I have and I have 2 signature lightcone of Kafka and archeron so who should I pull aventurine or fu xuan?', 'EN', 'FR'), 
    ('DAY 11 OF SAVING FOR WANDERER\ntechnically not saving for HIM. \nbut for his cons/signature weapon, so yeah...—\n\nBABYGOWRL ILL SPEND EVERY SINGLE THING FOR YOUUUU-\n\n\\t\\t\\t\\t\\t\\t\\t~`•Stay Nice•`~', 'EN', 'VI'), 
    ('Furina in Co-Op\nI did co-op to fight my boyfriend- i mean that totally not cute big puppet thing ()  and we won! My Furina may or may not have been the only one to survive the ordeal but that’s okay!  I’m a great teammate.', 'EN', 'JP'), 
    ('I FINALLY GOT A COPY OF AVENTURINE\nI lost my 5050 to Yanqing at 71 pity and pretty much lost hope, but I grinded for like 4 days straight, scrounged up about 20 pulls, and was able to get him at about 30 pity! No more trailblazer copium build yay :D', 'EN', 'DE'), 
    ("😭😭\nPov : you wanted neuvillette's weapon ", 'EN', 'JP'), 
    ('Day 18 posting Yanfei pics from the archives (Featuring Nilou!)\nYanfei s trying the power of TCG invitationals to manifest a Nilou re-run announcement for 4.7. Please and thank you Hoyoverse!', 'EN', 'TH'), 
    ("After not playing for 5 version. I Got this (it was sad for me..)\nGot Acheron before her banner ends but don't have  pulls saved up for adventurine. Clara on Standard. So sad, still no Bronya. I hate Clara. And finally, good things doesn't come for me, Since I'm not in the game for 5 versions there's many content to grind, I grind but lose 5050 on Adventurine banner (took 82 pulls, it's sucks right? Almost hard pity), totally got scam by Adventurine to go all in to get big", 'EN', 'FR'), 
    ('this event is about turning honkai beasts into food !!\nyeah, the honkai beasts, consecrated honkai lifeforms that turns people into zombies just by standing next to them, in oxia they get turned into food for its people to eat.oxia people are built differently. ', 'EN', 'JP'), 
    ("Hsr ships I hate part 2 (desc)\nAgain, it's about ships, not shippers so don't sh*t yourselves if here's a ship that you like, it's just my opinion about shipsI kinda like reading dramas in the comments so do y'all want me to make version with ships I love? ", 'EN', 'CHT'), 
    ('I can t beat MOC 10. I need tips.\nThose are all my characters that I use. I swapped out Silver Wolf for Bronya. Can someone give me tips on how I can improve.', 'EN', 'ID'), 
    ('Is he good with aventurine?\nI lost Jingliu 50/50 and now im stuck with choosing either Him or Dr Ratio. Im trying to make a 2nd team for MoC and PF', 'EN', 'RU'), 
    ('Fun times vs annoying mechanics\nA good solution to the challenging mechanics of this boss, with some breathing room for gamba phases.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'RU'), 
    ("Fischl. 8-11-11.\nAnother wave of upgrades for Mein Fraulein! Another one! ANOTHER ONE! And now she moves up to 8-11-11. Thus do I have a new project alongside Furina's final crown: getting Fischl to 9-12-12. All that is needed is mora and philosophies of ballad: all 36 of them.", 'EN', 'FR'), 
    ('Charlotte s picture taking\nAka Charlotte s journey in Fontaine', 'EN', 'VI'), 
    ("Please help me!\nHi guys, newbie here and I'm wondering what team composition to use and how to properly build them. I currently use Neuvillete, Xianling, Barbara and Razor/Sucrose (I'm helpless). Any help can be appreciated! Anyways, here are my heroes currently. ", 'EN', 'EN'), 
    ('WHAT THE HELL\nMy friend said  moist  so I said  moist  then I waited for her to say  moist  so when she didn t say  moist  I said moist again.....THEN SHE SAID \\ NO\\  THEN \\ NO MORE MOIST\\  THEN THIS HAPPENED.....I DEAD', 'EN', 'JP'), 
    ("Storage\nHoping my storage doesn't dieAlso hoping my PC can run it cause if my phone can't, atleast my PC might be able to 😓", 'EN', 'KR'), 
    ("Yanqing slayed / welt with stolen artifacts ...\nDon't know what to say just that yanqing carried the team ! The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'TH'), 
    ('Klee!\nKlee is one of the cutest Genshin characters with an explosive backstory! I just love her! But... I do miss her previous VA and walking style...', 'EN', 'ID'), 
    ('[HSR] SamPard Highschool AU\na silly little comic of sampard I made a while back\ninspired by art made by @/foxspritezz on twitter\nand on twitter I have many more stuff but it s not important now lmao', 'EN', 'CHT'), 
    ("Today I wanted to play with different brushes \nSo Kokomi was today's victim. I tried to draw a lightning strike in the back (since Inazuma is all about storms and stuff like that) but well it didn't turn out as good as I expected it to be but whatever", 'EN', 'KR'), 
    ('Journey to 1000 Pulls in F2P! Day 124\nI m currently trying to finish the Sumeru desert for good. It s been annoying me and I can t wait to start in the Sumeru Forest :D', 'EN', 'RU'), 
    ("HELP ME GET ARLECCHINO\nSo I just got Kazuha and I really want Arlecchino I need help exploring so if you could give your discord in the comments I would be extremely grateful. Ever since I saw Arlecchinos animation I've loved how we play her and she is my favorite character, I would hope to snag her and r1 but just her is enough. Thanks in advance!!! ", 'EN', 'CHS'), 
    ('Why is the hsr icon... um..\nWell, after I ghosted hsr for months on my pc, I noticed this little detail, the corner of the icon is.. yeah. I don t know what the heck, but hoyo never does this\n\nWHAT IS HAPPENING\nDO I HAVE A VIRUS', 'EN', 'JP'), 
    ('Done with achievements\nFinally after 3 years,I have completed all achievements till 4.5, and now 4.6 is just around the corner. The hustle is not gonna end anytime soon haha', 'EN', 'CHS'), 
    ("Aventurine or Ruan Mei\nI have 15k jades rn so I'm in a dilemma as to pull for our boy Aventurine or should I save for a rerun character which is most likely ruan mei. I am definitely getting firefly when she comes out so I reckon I can only get 1 of those 2 limited character in order to have enough jades for her. I enjoyed Aventurine story and character but I also like ruan mei mummy vibes and her kit is also so good especially for the SU ruan mei occurrence. Side note I am able to clear the current and previous moc 12 3 stars though I had to grind the rng for this current moc to prevent 1 character from taking too much damage ", 'EN', 'CHT'), 
    ('Spending 1100 days in Genshin Imapct ✨\nIt is a honor to play Hoyoverse game for this long and continue to play it till the end...We love you Hoyoverse, no matter what <3', 'EN', 'JP'), 
    ("Whyyyy does my genshin burnout have to overlap with the time I need to save for Arlecchino 😭\nI wish I could pause time because I haven't played genshin in months but I need Arlecchino soooo badddddddddd but not badly enough to load up the game and then I'll be so upset because the moment I get the energy to play genshin again it'll be right after her banner ends", 'EN', 'JP'), 
    ('Silver Wolf 🐺💗❤️ (Coser: SISO 小夕)\nCoser: SISO 小夕\nCoser twitter: https://twitter.com/xisaw_\nImage source: https://twitter.com/xisaw_/status/1781296080946372640/photo/1', 'EN', 'ID'), 
    ('Swan diving into achievement hunt\nFor this one I recommend using the current forgotten hall stages since so much dot in them that getting 20 stacks off of swan should be easy', 'EN', 'TH'), 
    ('Adventurine and Archeron Account Changers💯\nMy 1st time attempting MoC 12 went well with this team.. Feels good The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'RU'), 
    ('Elegant Ayaka ❄️ (Art by 椎名樱雪)\nArt by 椎名樱雪 on Pixiv, please go check out and send loads of support to the artist! \n\nSource: https://www.pixiv.net/en/artworks/117741073', 'EN', 'FR'), 
    ('.\nwriothesley and clorinde best duo frfr', 'EN', 'CHS'), 
    ('F2p team\nClara is really good at gambling.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'JP'), 
    ('slay\nxingqiu best support man like seriously ', 'EN', 'TH'), 
    ('Sir that is a Child…..\nAm I really doing this to a literal child!? Making a servant out of a child. This sounds like…..if you know you know.', 'EN', 'KR'), 
    ('Amrita pool\nI just got 600 primgems from making all the offerings of plume of purifying light which is only 36 you don t have to spend much time it s in the surrounding area only if you still haven t collected yet than than missing out on 600 primos (complete quest khvarena of good and evil before making this offering) \nbest of luck with farming', 'EN', 'EN'), 
    ("Pay Attention To The Event\nWhile promotional events rotate in and out of Honkai: Star Rail all the time, there's a good chance if you're paying attention you can earn a\xa0lot\xa0of\xa0Stellar Jade\xa0and even\xa0Star Rail Passes\xa0and\xa0Star Rail Special Passes\xa0just for interacting with the game. Requirements will change depending on the current timetable, but often you'll only have to login to earn rewards, which can lead to multiple free pulls.FOLLOW FOR MORE", 'EN', 'EN'), 
    ('yay\ncyno + tighnari best duo frfrfr', 'EN', 'ID'), 
    ("got 1186th today 🥳\nI thought I need to get all experimental drinks to get this achievement. There are 8 experimental drinks and I got ED#1 (+ salt, carbonated, og state)If I get the dc again I'll try getting the rest and see if there's another hidden achievement ", 'EN', 'VI'), 
    ('my kazuha pull!\ni got xiao at pity 30 after i got Jean, which im happy bcs i got him at early pity but lost my 50/50 at kazuha banner hurt a bit, it s fine tho since it s qiqii (see ya at the next banner kazuha :D)', 'EN', 'JP'), 
    ("Imagine what Aventurine would be like in his daily work!\n I feel like Aventurine prolly starts his day by planning out everything for the day ahead. He'd walk around the place with confidence, wearing a smile that hides his true thoughts and intentions. If there's a meeting, he's likely the pne encouraging everyone to think outside the box and come up with new ideas. At the end of the day, he'd prolly feel satisfied knowing he made smart decisions throughout the day.Ps: I'm new to HSR and haven't done his story quest yet, but absolutely love his gameplay! ", 'EN', 'DE'), 
    ('Magical place ;\u2060)\nSuch a beautiful place don t you think? :D', 'EN', 'FR'), 
    ('Day 7 Saving Primogems ( April 20 2024 )\n4796 primogems, 5 rainbow fate, 33 blue fate, AR27', 'EN', 'TH'), 
    ('STELLE — — AVENTURINE — — swapping clothes series give a name\nanyways I’m sorry I didn’t post much lately I was busy with exams anyways here’s a stelle and aventurine I don’t ship them this is so risky please I’m sorry aventurine topaz shippers and aventurine ratio shippers\n\nY’know this was so risky to post bc I know those shippers are gonna go get pitchforks. Anyways Im gonna start a series called (changing clothes series and unrelated to ships)\n\nAVENTURINE COME HOMEEEEE', 'EN', 'CHT'), 
    ("Acheron relics\nHi there so all I want to ask is that can you guys like send me a pic of like an Acheron relic setup? What I mean by this is like what is the literal best setup from the main bonus to the extras. So what would be like a good bonus in the extras in a way like for instance it's like 2 ATK 1 crit dmg and 1 crit rate, stuff like that.", 'EN', 'FR'), 
    ('Arlecchino Please Come home 😭\nSaving for Arlecchino Day 20 after getting Kazuha on pity 76. TBH I m always at red pity. 😭 Just please for one just please Hoyo gime ‘Father’ Arlecchino at soft pity I BEG YOU', 'EN', 'CHS'), 
    ("Childe in Hoyofair !!\nI know I'm late and it's been quite long since this came out but I'm still obsessed with it !!I mean he looks so good, he's a pretty boy ! I'm so happy because we got so much fatui content lately and I love them so much, it's my special interest so yeah this is everything for me !And here he's with Father !! Arlecchino !  Hoyofair gave us content for two Harbinger as the same time ! It's been so long since we had someAnd Childe, the outfit he was wearing is incredible, just look at the concept art :MY PRECIOUS It just look so good on him !! The color, the pose, the shirt, his name written on it, the pants, everything.And also it's the second time we get a rockstar Childe with this colors scheme MY BOY LOOK AT HIMAnd notice how he handsome in both of them ! My boy's just so perfectThat's all ! I just wanted to make a post about it because it hasn't left my mind... Thanks for reading, go read Childe's lore now !", 'EN', 'RU'), 
    ('He s so goated in game guys pull for aventurine\ni use blade, ratio, aven, loucha team, is it ok???', 'EN', 'JP'), 
    ('In the recent polls\nBaizhu was in the lower ranks. But before his release, people were excited and hyped for him to be playable.\nAnyway, I started liking Baizhu s character from his story quest. That s the most beautiful story quest of all.\n\nPS. This is just my opinion but the personality of the Eng and Jap VA are so different from each other.', 'EN', 'DE'), 
    ('EARLY PITY AGAIN!\nwell, after losing to Acheron s banner 2 times in a row I feel like I deserve this...\n\nI got him at 9 pity, Acheron E1 on 4 pity and her lightcone on 10 pity. I got Jingliu guaranteed at like 76 pity\n\nbruh it s hard when you are only a f2p player and a newbie', 'EN', 'CHS'), 
    ('Who s Excited for Robin?🤩💜\U0001fa75🔮🥺\nComment down below if u are excited!🧐👇🏻✨', 'EN', 'CHT'), 
    ("Please help me with building Yaoyao for hyperbloom!\nI want to run a hyperbloom team with dendro mc , Yaoyao , Xingqiu  and Shinobu .Dendro mc is running 4pc Deepwood. Should I give Yaoyao 4pc Deepwood too? Does the 4pc passive even stack? If not, then what should I use on her? Will 4pc Gilded Dreams work on her? Or is 2pc 2pc em more preferable? Or maybe 2pc hp 2pc em?Also, should I run double dendro or should I switch out Yaoyao for someone like Raiden instead?I'm only now deciding to test out dendro teams, since I was pretty content with my mono anemo or vapourize teams so far lol. All I know is that I should stack em for dendro teams and that's it, so any and all help will be much appreciated ", 'EN', 'TH'), 
    ("Hardest MoC yet.\nI had to use Pela's skill a lot in order to clear this.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'VI'), 
    ('it s complete\nThe last imaginary member finally came home', 'EN', 'JP'), 
    ('Happy update\nladies, gents and non-binary friends, I got him', 'EN', 'TH'), 
    (' Catalyst For Life \nSAUCE: A funny screenshot I took when playing Honkai!\n\nEditing some of these on the phone is tricky, usually the more \\ edit intense\\  poorly made memes I work on the iPad s pro create, but I only have so much spare time... \n\nI even missed the window for a funny Geo joke, well I guess I can use it on the next Geo release.\n\nEdit: Forgot to mention the whole \\ jab, jape, or  joke \\  is that every now and then when streaming someone tries to sell me their artwork, it s really weird. especially since I ve added it to the \\ first time chatter\\  rule box to say \\ yah don t ask for socials or sell stuff\\ ', 'EN', 'TH'), 
    ('Are these stats good?\nThese are my stats for neuvillete. He has around 37.5k hp w hp%/hp%/cd% with the mh 4pc set and ballad of boundless blue weapons\n\non a side note should i get his signature weapon as well with these stats?', 'EN', 'VI'), 
    ('Day 57 of Posting a Homemade Meme Until Hoyo Makes me a Voice Actor\nWant Jinglius lightcone this rerun…', 'EN', 'TH'), 
    ('Pulling for who\nGuys any suggestions who should I pull', 'EN', 'JP'), 
    ('❄️Ayaka in idle mode, she is so cool~\nI remember meeting her and how her beautiful dance captivated me. \nWhat a memorable and noble performance. \nRecently, I ve started playing her again! I ve missed you. I caught a lovely shot of her in idle mode, observing Ayatos Haran Geppaku Futsu, his main weapon.\nI let her borrow it for a moment before giving it back to him.\nFor today, I ll be Travelling around, floating calmly in Fontainian waters, perhaps some gently walks along the Mondstadt cliffs, or even back at the forge backing a couple of homemade weapons, perhaps Finale of the Deep or... Tidal Shadow. \nWho knows what else! But what can be guaranteed, I ll be sure to return to Wangshu Inn afterwards to eat a little almond tofu and maybe brew up some of my own minty fruit tea. 🍵', 'EN', 'TH'), 
    ('ShouldI do Ship art?Apparently its a bit controversial 😭\nI’ve made like one chilumi post in the past but i do have some other ships i enjoy… but….Ive seen quite a few fights over the topic of shipping though and i dont want to anger anyone 😭😭 what should I do? (Header pic for attention)(might chicken out and delete the post idk)', 'EN', 'TH'), 
    ("Sad.How I been\nTo those who did or didn't care on how I was doing honestly it didn't really matter I guess I'll just go in a debt we all know life sucks right", 'EN', 'CHS'), 
    ('My opinion in character s redesign/fanart\nY\'know.. you\'ve probably seen many artists,redesigns etc. changes character\'s real skintone..I saw many good art and redesign but like.. changing character\'s skintone is not a good thing for me tbh...I saw a few redesign and they changes character\'s real skintone.. like- They even claim the half of the comments are being \'rude\'.But.. half of the comments are actually spitting \'facts\' and real \'truth\' on their art..They changed the design and it\'s alright but the skintone is not giving.. .People be mad MADDD if artists changes dark skinned characters and turn them white- BUT if the artist changes light skinned characters and turn them black.. "oH yEaH it\'s OkAy"..like seriously???- .I\'m not being racist but- what\'s the purpose on hating whitewash if blackwash could get away with it. Use logic please!.I know this is a GAME but- it has cultural relations and I think it is NOT OKAY to change character\'s real skintone.. Why can\'t some people appreciate the original skintone? Is it hard?? Is it difficult?!.Just- think logically.. not all characters from specific area are SUPPOSED to have the skintone you are expecting...I\'m completely disappointed by some of the community that went too far with art/redesign...It\'s just not fair and equal y\'know? ', 'EN', 'FR'), 
    ('WHY Fortune slips are key (Screeching rn)\nI’m screeching\n\nGuys narukami shrine is the way to get early 5 stars in 50/50s\nI got you 5 pity after raiden and Neuvillette 5 pity after kazu on days where I got great fortune. Similarly, on a day I didn’t I got a weird tall red Nahida.', 'EN', 'CHS'), 
    ('itto s long last brother\nItto and Tengen would be besties tbh', 'EN', 'CHS'), 
    ('Sumuru ending theory\nSo I was watching a bunch of old genshin content and I found the trailer where all the harbingers were introduced and the iconic scene of doctore near the buring irminsul tree and I was confused on why they\'d show that but not put it in game so I did more deep diving.In another post we got what each of the final acts for each region would be called and sumuru final act is supposed to be "truth amongst the table of pruna" but the last one we had was "akasha pulses the kalpa flames" which does not seem to match upIt would make sense now cause there adding in the next cyno quest which seems very mysterious and with all the odd kanierh items that we have seen in sumuru it seems a bit unfinishedAgain this is only my theory so what do you all think of it?', 'EN', 'JP'), 
    ('Savings :3\nReady to b stepped on by cappuccino', 'EN', 'JP'), 
    ('Day 13: That would certainly be interesting.\nHe would keep posting about current investigations, promote Serval s stuff oh and don t forget that he would constantly be trolled by Sampo in his comment sections.', 'EN', 'VI'), 
    ('Should I sacrifice her atk to get higher er and change her weapon to favonius?\nHow much er is good for shenhe?', 'EN', 'JP'), 
    ('Day 11: Water/Anything that isn t water.\nI wholeheartedly believe he will shrivel up and die like a raisin if he ingests anything that has less than 50% water in it.', 'EN', 'ID'), 
    ('Delusional or just Unlucky??\nIs it just me or does HSR keep getting harder for no apparent reason? I mean like, I\'ve used the same team comp for SU, Swarm, and Gold And Gears and I feel like they\'re just not dealing the same Damage as before. I\'ve upgraded my talents for wach but that still didn\'t work, I\'ve tried to level up relics but due to my insanely bad luck, all of it rolled to Def. Even with my DHIL Swarm was so easy but now it felt like a huge pain in the ass. Not to mention the rng of this game, again is it just me or if I either pick a path, either I get insanely lucky and get all blessings from that path or I get insanely unlucky and get every blessing other than the specified path. It clearly says there in the description "Increased Chance of obtaining blessings in *This specified Path" for example, i choose Remembrance, but then I get Nihility, Destruction, Hunt, even Preservation but not Remembrance itself?? It feels like the game is watching you and intentionally does not want you to get the blessings you need', 'EN', 'DE'), 
    ('UPDATE! Got Kazuha as well!\nI got Neuvillette at 24th pull. I had around 40 fates left and I went for Kazuha after saving some more and lost the 50/50 at hard pity (80 something) and got Keqing. \n\nThat was 10 days ago. Since then I saved like a mad man & got Kazuha finally at 81 pull 🥲. In process, I 100% explored 3 regions of Fontaine. \n\nNow I am gonna save for Natlan characters.', 'EN', 'DE'), 
    ('posting for points! (day 2)\nalso drew a simple sketch cuz why not~', 'EN', 'KR'), 
    ("Siobhan\nOriginal artist: -Yue-I see that we don't have a topic for this Lady who is as cool as Serval. Let's fix this. (Siobhan is cooler IMO, but I'm biased, so let's trust March on this and follow her opinion) Source:https://yue62170.lofter.com/post/201d88d1_2bb80dbab", 'EN', 'JP'), 
    ("HELP NEEDED!!!\nGuys! I just lost my bird who was my birthday gift and one of the only gifts my late mother left. Im having a hard time trying to overcome his death and am really depressed cuz he was not a pet, he was my companion, my family. Im a hardcore but I'm still screeching after 3 days. Cause of death: Annoying, spoiled, little brother to whom you can't even touch, if so instant death.Got any recommendations on how to calm my emptiness?", 'EN', 'TH'), 
    ('wip Aven\nI love aventurine sm but here s a wip', 'EN', 'JP'), 
    ('Yao Yao Genderbend !!\nhere s yaoyao!! \n\nsorry this took so long, I was genuinely stuck in what to do with her, and to me her hair looks off but I wouldn t know what to fix anyways, but I like how the pants turned out!! still pretty girly, but hey, can t really see yao yao changing a lot anyways.\n\nalso a little disclaimer, i am still learning! I ve been seeing so many positive comments, and I am so grateful for everyone who s been so nice to me while im figuring this stuff out <33 \n\nas always, requests are open!! been getting a few of them, so warning that it might take a bit ^^', 'EN', 'JP'), 
    ('profile pic\nThey (HoYoLab moderators) approve this picture of Gallagher after his yawn as my profile picture here in HoYoLab. \n\nThanks and nice!', 'EN', 'KR'), 
    ("Spiral Abyss 4.5, Nilou and Alhaitham Floor 12-3\nbaizhu tried to save furina and those 2 dancer won't let him... 33hp baizhu, the lowest that i've ever got meanwhile zhongli with his plunge 555 ", 'EN', 'JP'), 
    ('Arlecchino doll\nI better not lose the 50/50 now... ', 'EN', 'DE'), 
    ('The only things keeping me sane\nwhat the title said xd\n\nThe keychain plush can be found on the Temu website/app. The pillow can be found on Amazon.', 'EN', 'FR'), 
    ("Just got Artem s bday card in six pulls...\nI was just doing it for fun to see what I'd get...I didn't think I actually would, I'm in utter shock and disbelief..So cute!!!", 'EN', 'FR'), 
    ("In search of new friends\nlooking for some new friends that are as interested, for Genshin and Star Rail, as me. Doesn’t have to be serious just chill vibesI'm on EU serversdiscord: dennis2300", 'EN', 'TH'), 
    ("I don t recommend my build\nI'm just trying this lineup thing, please ignore it. thank youThe content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~", 'EN', 'ID'), 
    ('Your worst nightmare\nYour worst nightmarePov: you need 1 more wish 😭 ', 'EN', 'TH'), 
    ('4.5 Abyss - Eula Hyperfridge / Lyney Mono Pyro\nSo, after playing physical Eula, I wanted to see, if my account would be ready for this. Since I am passively farming Flower of Paradise Lost for Thoma, I will shortly test how the artifacts I already have work on Shinobu.\n\nWhen Lyney came out, I thought about getting him to C2 but wanted to safe primos for more upcoming Fontaine characters. Since we still don t know when Clorinde will be presented and I have 170 wishes, maybe I roll to at least one 5-Star and keep safing on a 50/50 loss.\n\nPropably I will only do this, if Lynette on the new banner.\n\nI m not really interested in Arlecchino, to be perfectly honest. ', 'EN', 'TH'), 
    ('Another Hyperspecific Poll for Genshin Players!\nBringing this back because why not, this time featuring a proper cover photo (If you have alt accounts, please choose pertaining to your main account)', 'EN', 'DE'), 
    ('he looks so pretty in casual wear I cant-\nomagajd please your hand in marriage?!?!', 'EN', 'TH'), 
    ('Official 2024 Calendar ❤ Artem\nFinally got the time to unbox this! This arrived last month or February iirc and I m in love with this calendar design already compared to the 2023 version!\n\nThe cards / artprints can be swapped very easily and they re very good quality! The prints are so beautiful 🥺🤍', 'EN', 'CHS'), 
    ('Thank you...\nThank you so much for 400 views!! ', 'EN', 'EN'), 
    ('WHAT.... silly wisher is insane\nHOYO PLEASE BE GENEROUS WITH US PLEASE HOYO😭', 'EN', 'TH'), 
    ("When in doubt, rainbow\nRainbow-coloured first aniversary cake#anniversary cake#Honkai Star Rail: First Anniversary CelebrationI have no idea what I'm doing", 'EN', 'CHS'), 
    ('My boys with Eidolons :3\nI am warping for eidolons of favorite boys only XD', 'EN', 'VI'), 
    ('LYNEY MADE CHESTS APPEAR MAGICALLY\nLyney: Want to see a magic trick??\nMe: Sure, but DON T MAKE STUFF DISAPPEAR\nLyney: *Cutest smiles and makes all hillicurls disappear*\nMe: WELL WHAT IS THE TRICK?! \nLyney: This! *proceeds to show me the 3 chests*', 'EN', 'RU'), 
    ('Looks like it s time to level Barbara up.\nFinally I managed to get a healer to this stage. ', 'EN', 'CHT'), 
    ('Recommend teams please!\nHi! what other characters would any of you recommend if I want to play aventurine and jingyuan in a team? I’m not really good at this game so any help is greatly appreciated :) ', 'EN', 'DE'), 
    ('Lucky E1 S1 in less than 200 pulls\nWon all the 50/50. Luck is on my side.', 'EN', 'JP'), 
    ('Genshin I order you to fix this!\nGenshin I order you to fix this!\nIn the 4.5 update I couldn’t log into my account no matter what I did! Please fix this bug.', 'EN', 'ID'), 
    ('Need Klee!💕\nIt has been forever and a day since I\'ve actually played, but Klee is my favorite "new" character (new for me, obviously lol).Hopefully, I\'ll get to enjoy her explosively cute personality and dynamite outfits~!😂💕', 'EN', 'TH'), 
    ('For Aventurine backgrounds ~\n1. What do you want to say to Aventurine after the Main Story in this patch?\n  → Please stay safe and share me your luck pleaseeee.\n2. Imagine what Aventurine would be like in his daily work!\n  → A full time gambler who always win!\n3. If you were to describe Aventurine using playing cards, which card you think he resembles?\n  → The ace of spades!', 'EN', 'RU'), 
    ("Almost 1 night just for find this chest\nCurrently trying to find all the chests in Penacony before there is an update for the new map I've gone around 3 times this map using Topaz and only 1 chest is left, it turns out it was the chest at the start when I arrived at the map, I thought I had taken it during the quest ", 'EN', 'FR'), 
    ('WAR IS OVER!\nfinally no more signora and that shi', 'EN', 'JP'), 
    ('Reminder about Penguin Boy🐧\nAs we get closer and closer to 4.6, please be reminded that Freminet, the sweet, shy, overlooked House of the Hearth orphan, BLOCKED a blow by The Knave (4th of the freaking Fatui Harbingers) They say you should be scared when the quiet kid snaps but personally, I can not wait to see how bad@ss Freminet is gonna be in the next patch ', 'EN', 'TH'), 
    ('This dude just give me what??\nI ve been strengthening my straightness by \\ ignoring\\  the mails i got from male characters and taking only gifts from waifus for half a year or so. And this dude just give me dream solvent like WHATTT?. Should I take this rare item or not?', 'EN', 'JP'), 
    ('Take that, Gorilla!\n1st half was easy, Acheron sweeps. 2nd half, used an almost mono-Imaginary team with Ruan Mei to quickly break the gorillas and Bronya. So this is the power of a limited sustainer.The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'CHS'), 
    ('🤔🤔🤔\nhow my star rail pulls went...', 'EN', 'ID'), 
    ('should I start a dtiys contest?\nI’ve been thinking abt starting one but idrk rn…the poll ends in a week. if there’a more yes’s than nos then there’ll be a dtiys. the character that I’ll use for this dtiys is Wynter (my hsr oc) since I’m still working on her bro and my first one', 'EN', 'DE'), 
    ("I have 50 pulls should I pull Aventurine OR Jingliu \nHELLO~~~Can anyone suggest me who should I pull Jingliu or Aventurine since I'M FP2 PLAYER AND I ONLY HAVE 50 PULLS", 'EN', 'CHT'), 
    ('Full on auto!\nGot this team on auto and got full stars!The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~', 'EN', 'DE'), 
    ('Perfect Coin Flip\nKaeya’s idle animations are my favorite!\n\n(I think I was trying to capture Chenyu Vale at a distance, but at least you can see Fontaine from here!', 'EN', 'CHT'),
    ("""Dear Traveler,      

The Genshin Impact Version 4.6 <span class="notranslate">"Two Worlds Aflame, the Crimson Night Fades"</span> update is coming soon. Registration for the Twitch Livestream Event has started.        

        

Event Timeline      
Registration Period: April 19 at 19:00:00 – April 26 at 15:00:00 (UTC+8)        

Streaming Period: April 24 after the version update to May 14, 23:59:59 (UTC+8)     

Note: Participants who successfully register before April 24 at 00:00:00 (UTC+8) will be able to start streaming after the Version 4.6 update. Participants who register after April 24 at 00:00:00 (UTC+8) will need to wait until April 27 at 00:00:00 (UTC+8) to start streaming.        

Reward Calculation: May 15 – May 30     

*Primogem rewards will be delivered to valid participants' accounts no later than 30 business days after the reward calculation period has concluded.

*Cash rewards will be delivered to valid participants' accounts no later than 45 business days after the reward calculation period has concluded.       

Email Notification: Participants will receive a welcome email with event details from April 26 – April 30. Reward notification emails will be sent within 30 business days after the reward calculation period ends, to the accounts of all participants. Please pay attention to these messages.       

        

Event Details       
1. Participants who meet the following conditions will be able to obtain the corresponding rewards:     

a. Sign up for the Version 4.6 Twitch Livestream Event      

b. Link an Email to a HoYoverse account     

c. This event is open to Genshin Impact accounts registered on the following four servers: America, Europe, Asia, and (TW, HK, MO).     

d. During the event, participants must stream in the Genshin Impact category on Twitch for a total duration of 6 hours or more in order to qualify for the "Start Streaming" and "Aim for the Leaderboard" rewards.     

2. Participants who successfully register before April 24 at 00:00:00 (UTC+8) will be able to start streaming after the Version 4.6 update. Participants who register after April 24 at 00:00:00 (UTC+8) will need to wait until April 27 at 00:00:00 (UTC+8) to start streaming.       

3. Primogem rewards will be delivered to valid participants' accounts no later than 30 business days after the event has concluded.     

4. Any form of cheating or negligence within the community, event, or platform will not be tolerated and can result in indefinite suspension from future or related events.     

a. Example of cheating: Streamer A logs into Genshin Impact and is AFK for 24 hours.        

b. Example of negligence: Streaming games/content that are not related to Genshin Impact in the Genshin Impact category in an attempt to get Primogems.     

5. Disclosing or discussing the content of an upcoming release will not be tolerated and can result in indefinite suspension from future or related events.     

        

Register Now
        

Event Notice        
1. Registration in this version of the event is required in order to participate in the event.      

a. Each registration is independent and applies only to the event of a specific version. Registrations made for a previous version cannot be used for the event of the next version.        

b. HoYoverse accounts must be linked to an email for contact purposes.      

c. Participants are responsible for ensuring the accuracy and validity of their information. The Genshin Impact team will not be responsible for any mistakes and related disputes arising from participants.       

2. The Genshin Impact team reserves the right to determine the eligibility of participants before, during, and after the event.     

a. Rewards will not be awarded if the event registration is not completed.      

b. Those who do not meet the minimum requirements will not be eligible for rewards.     

c. Participants suspected of unfair advantage or engaging in forms of abuse will be immediately disqualified.       

d. This event is open to Genshin Impact accounts registered on the following four servers: America, Europe, Asia, and (TW, HK, MO).     

3. The Genshin Impact team is responsible for determining participants' eligibility in receiving prizes.        

*Submission of multimedia files/videos will not be required after the event concludes.      

4. By participating in this event and submitting information, participants agree to official access and disclosure of participant information for the purpose of administration and prize distribution.     

5. By participating in this event, you agree to:        

a. The terms and conditions (https://hoyo.link/cmTiFBAL)        

b. Genshin Impact's Privacy Policy (https://genshin.hoyoverse.com/en/company/privacy)       

c. Twitch's Privacy Policy (https://www.twitch.tv/p/en/legal/privacy-notice)        



Watching Rewards        

Watch a certain number of hours of streams during the event in the Genshin Impact category on Twitch to win the following rewards!      

Rewards can only be collected after linking a HoYoverse account with a Twitch account, enabling Twitch Drops, and watching a certain number of hours of eligible Genshin Impact streams. Each type of reward is limited to 300,000 in quantity.     

*Note: Twitch Drops is separate from the Twitch Livestream Event and thus Drops rewards can be claimed immediately after achieving the listed criteria from the [Registration] website.     

*More information about Twitch Drops:https://help.twitch.tv/s/article/mission-based-drops       

*Each tier of Twitch Drops rewards is limited to 300,000. First come, first served!     

        

Streaming Rewards       
*Twitch Streamer Recruitment Events Rewards will be delivered no later than 30 business days after the event has concluded.     


Streaming Duration Event Details        
When participants reach a certain number of stream hours during the event, they will get a chance to receive the corresponding rewards.     

Note: "6 hours" is defined as streaming at least 6 hours in Twitch's Genshin Impact category throughout the event.      

For further clarification: Reaching 6 hours equates to Primogems ×200. Reaching 9 hours equates to Primogems ×450. Reaching 12 hours equates to Primogems ×800.

Reaching 30 hours equates to Primogems ×1,600.      

*The reward is limited to 19,000 sets for 6 hours of live streams.

*The reward is limited to 13,000 sets for 9 hours of live streams.

*The reward is limited to 11,000 sets for 12 hours of live streams.

*The reward is limited to 3,000 sets for 30 hours of live streams.

*If the number of rewards reaches its limit, winners will be selected based on the average number of concurrent viewers.        

        

Consecutive Check-Ins Event Details     
During the Live Streaming Phase, participants will gain a milestone if their stream time within an "Event Week" reaches 3 hours.        

Every "Event Week" starts on Wednesday at 00:00:00 (UTC+8) and ends on the following Tuesday at 23:59:59 (UTC+8). See below for details (*Times provided are UTC+8).        

*Week 1: April 24 after the version update – April 30 at 23:59:59       

*Week 2: May 1 at 00:00:00 – May 7 at 23:59:59      

*Week 3: May 8 at 00:00:00 – May 14 at 23:59:59     

Participants will obtain the milestone(s) once they meet the event requirements.        

Participants can obtain only one milestone during each "Event Week" and a total of three milestones during the entire event duration.       

*The reward is limited to 15,000 sets for 1 week of reaching the milestone in the Consecutive Check-In milestone event.

*The reward is limited to 12,000 sets for 2 weeks of reaching the milestone in the Consecutive Check-In milestone event.

*The reward is limited to 10,000 sets for 3 weeks of reaching the milestone in the Consecutive Check-In milestone event.

*If the number of rewards reaches its limit, winners will be selected based on the average number of concurrent viewers (CCV).      

*"Streaming Duration Challenge" and "Consecutive Check-Ins" rewards can be obtained together with "Aim for the Leaderboard" rewards.        




*"Most Hours Watched Leaderboard (HW)" and "Average Concurrent Viewers Leaderboard (CCV)" rewards can be obtained at the same time. The results of the two rankings are counted separately.     

Note: Channel's Rank performance will be measured within the event's duration.      

*Hours Watched Leaderboard (HW) defines the total number of hours watched of Genshin Impact category live streams broadcast by participants throughout the event.       

*Average Concurrent Viewers Leaderboard (Avg. CCV) defines the average number of concurrent viewers of Genshin Impact category live streams broadcast by participants throughout the event.     

*Cash rewards will be issued via PayPal transfer. After the event ends, please be sure to check the official winner notification email that participants can use to submit relevant information to obtain prizes.       

        

Event FAQ       
Q1: Is registration required to participate?        

A1: Yes. Registration is required for this event. (Latest Updates on Apr. 30)   

        

Q2: How do I link an email address with my HoYoverse account?       

A2: Go tohttps://account.hoyoverse.com and log into your HoYoverse account. Confirm and verify your email address in the "Account Security Settings" submenu.       

        

Q3: Will multimedia files/video submissions be required after the event ends?       

A3: No. Multimedia files/video submissions are not required.        

        

Q4: Can I stream immediately after registration?        

A4: Participants who successfully register before April 24 at 00:00:00 (UTC+8) will be able to start streaming after the Version 4.6 update. Participants who register after April 24 at 00:00:00 (UTC+8) will need to wait until April 27 at 00:00:00 (UTC+8) to start streaming.      

*If participants start streaming before the specified time, the stream data will not be counted.        

        

Q5: How can I redeem for cash rewards?      

A5: Participants will receive a notification email with their event rankings after the event ends. Participants can redeem for cash rewards by providing information required in the email.     

        

Q6: How will I be contacted?        

A6: You will be contacted via the email address indicated during your registration. We recommend that you check that your inbox allows you to receive emails from @hoyoverse.com to prevent messages from appearing in your junk mail.      

        

Q7: Why haven't I received any emails related to the event?     

A7: (a) Please make sure your email address is linked to your HoYoverse account.        

(b) Make sure you have not unsubscribed from official Genshin Impact emails. If you have unsubscribed, please contact Customer Service.     

(c) Check that the e-mails have not arrived in your spam or junk mail.      

(d) Ensure that the email address you use is the one linked to your HoYoverse account.      

        

Q8: If my region is not on the list of eligible regions for this event, is it possible that I will not receive any rewards?     

A8: If your region is not in the list of eligible regions for this event, you will not be able to obtain the corresponding rewards. For details on eligible regions, please refer to the relevant clauses via this link: https://hoyo.link/cmTiFBAL     

        

Q9: Can I get the cash prizes if I don't have a PayPal account?     

A9: Unfortunately, this is not possible. This event only uses PayPal as a means of money transfer. We recommend that you open a PayPal account in advance.      

        

Q10: If my channel is closed, will this affect my eligibility for the event?        

A10: Yes. If your channel is not set to public (closed or private) during the event, your event eligibility will be affected.       

        

Q11: Can two or more different UIDs share a Twitch channel?     

A11: No. If multiple different UIDs share a Twitch channel, only the last UID registered for the event will be eligible for rewards.        

        

Q12: Is there a quick guide to streaming on Twitch?     

A12: Yes. Please refer to this website: https://www.twitch.tv/creatorcamp/en/setting-up-your-stream/quick-start-guide-to-streaming-on-twitch/       

        

Q13: How do I choose the Genshin Impact category on Twitch for my stream?       

A13: PC - Once logged into your account, go to the "Creator Dashboard" by clicking on your profile picture. Then select "Stream Manager." On the right, you will find the "Quick Actions" tab where you can select "Edit Stream Info." A window will open where you can make the necessary changes to your stream. Select "Genshin Impact" in the "Category" section and click "Done" to save!      

Link: https://dashboard.twitch.tv/stream-manager        

More information: https://help.twitch.tv/s/article/creator-dashboard        




Mobile: Through the Twitch App, select the "Stream Games" button, then search and select the Game title "Genshin Impact." Next, complete the settings for your live stream. 

    

Click here for more information on the event:https://hoyo.link/7fTiFBAL 
""", 'EN', 'CHS'),
    (""""Two Worlds Aflame, the Crimson Night Fades" Version 4.6 Strategy Guides Contest

Hello, Traveler!

Version 4.6 "Two Worlds Aflame, the Crimson Night Fades" is now online. Come unlock new adventures today! Also, the Strategy Guides Contest for the new Version has begun today~

Guide Themes
Theme 1: Character Guides

Content related to characters such as Character Skill explanations, how to build and ascend them, how to get the hang of their play style, party composition recommendations, etc.

Corresponding Topics: #Character Guides#, #Arlecchino#, #Lyney#, #Wanderer#, #Baizhu#, etc.

Theme 2: Quests & Exploration

Detailed walkthroughs of World Quests, Story Quests, and other quests, as well as guides about unlocking achievements, open-world exploration, puzzle-solving explanations, etc.

Corresponding Topics: #Quest Guides#, #Exploration Puzzles#, #Achievements#, #Easter Eggs#, etc.

Theme 3: Event Details

Guides related to the Version 4.6 events.

Corresponding Topics: #Iridescent Arataki Rockin' for Life Tour de Force of Awesomeness#, #Windtrace: Seekers and Strategy#, #Specially-Shaped Saurian Search#, #Vibro-Crystal Applications#, etc.

Theme 4: Other Guides

Spiral Abyss Challenge sharing, tricks for defeating monsters/bosses, Weapon and Artifact building advice, ingredient and book gathering tips, Genius Invokation TCG all-series card reviews and Heated Battle Mode guides, etc.

Corresponding Topics: <span class="notranslate">#Spiral Abyss#</span>, <span class="notranslate">#Bounty Handbook#</span>, <span class="notranslate">#Genius Invokation TCG#</span>, #Other Guides#, etc.

Note: The details for the four guide themes given above are provided for Travelers to refer to when creating their guides. All types of guide content will stand a chance of winning rewards. In this Strategy Guides Contest, guides that are related to the new Version content (including the new character and events) will be more popular~

Event Duration
Submission Period: April 24, 2024 – June 2, 2024 23:59 (UTC+8)

Judging Period: June 3, 2024 – June 18, 2024

Results Announcement: June 19, 2024

Primogem rewards will be issued within 15 business days of the results being announced.

The estimated time for merchandise rewards delivery will be within 60 business days of the results being announced.

Event Rewards
Gold (5 Winners)

Primogems ×6,000·+ Mona Figure (Mirror Reflection of Doom) + Kamisato Ayaka Impression Apparel Series Umbrella

Silver (10 Winners)

Primogems ×2,000·+ FES 2023 Series Finger Puppet Keychain (Full Set) + Lyney Grin-Malkin Cat Moving Toy

Bronze (20 Winners)

Primogems ×1,000·+ Nilou Laptop Bag + "Jade Moon Upon a Sea of Clouds" CD Set + "Fleeting Colors in Flight" CD

Participation Prize

HoYoLAB - Genshin Impact Strategy Guides Contest-Exclusive Avatar Frame (30 days)

Judging Rules
1. The evaluation will be carried out by the guides judging team.

2. The official organizer will assess the strategy guides that meet the criteria on the basis of various factors, such as their timely effectiveness, completeness, content accuracy, clarity of explanation, applicability, composition, and aesthetics of the layout. Therefore, it is possible that not all awards will be given out.

3. If a prize-winning entry is disqualified due to violation of contest rules, the official team will not select a substitute winner.

Works Criteria
I. Submission Criteria

Entries must be posted through the Event Details page during the submission period. Entries posted after the deadline or posted anywhere other than on the Event Details page will not be considered.

II. Content Criteria

1. The guide should be rich in content and contain various images. They must include at least 5 images.

2. The main content of the submission must match its title. The content should be laid out in a clear and logical manner, neatly structured, and should not contain any major factual errors. Any form of copying or plagiarism is prohibited.

3. The main text must contain specific guide-related content. Guide Collections that simply redirect to other guides (for example, collections that only contain links, etc.) will not be considered eligible.

4. Entries may contain GIFs or videos to make the guide more interesting. Submissions with quality GIFs and videos may earn bonus points!

5. If a video that is longer than 3 minutes and contains voice or text commentary is inserted in the post, the requirement of at least 5 images for a post is no longer applicable.

6. The content of the video must be original and its description on YouTube must indicate "This video was made for the HoYoLAB Strategy Guides Contest, here is the link of the post: ...". Please include the link to your post in the video description, otherwise the video will be deemed as misappropriated work.

III. Other Criteria

1. Your guide must not contain fan art created by a third party. Such publications will be deleted. You may only use official images, screenshots from the game, or original illustrations in your guide.

2. Any misappropriation of another person's work is strictly prohibited. Posts that have been reported and proven to contain plagiarized or copied content will be removed immediately. Users who have violated the rules will be permanently banned from participating in future community events.

3. Entries containing content that violates the rules of the community will be handled in accordance with the Community Rules.

Event Guidelines
1. Traveler, please pay attention to HoYoLAB's System Messages, as information of merchandise prize-winners will be sent out via such messages. We ask prize-winners to provide their shipping address according to the prompts stated in the system message. Prize-winners who have not provided their address within the specified time frame will be deemed to have voluntarily forfeited their merchandise prizes.

2. Please go to My Information > Information Management > Genshin Impact in HoYoLAB to fill in your Genshin Impact UID ahead of time. If Primogem-winning Travelers have not filled in their UID or filled in the incorrect UID after the list of winners is announced, they will be deemed to have forfeited their Primogems reward.

Other Details
1. By participating in this event, users grant the organizer the right to distribute the content of their strategy guide online or offline. The Genshin Impact team may publish some outstanding works on HoYoLAB from time to time, adding them to the featured posts and recommendations on the home page. Featured or recommended works are not related to event prizes. The issuance of rewards is based on the final evaluation results. The content creators retain the right to include their names in their guides.

2. Each participant can submit multiple strategy guides, but only one prize will be awarded per UID. In the event that the same strategy guide wins more than one prize, only the highest prize will be awarded.

3. The criteria for submissions and other criteria may be supplemented in the case of disruptive actions to the community or unfair submissions. In this case, these additions to the criteria will be applicable to all entries submitted prior to the supplementation.

4. The event organizer will bear the delivery costs of merchandise prizes. Prizes being shipped may be subject to customs duties in accordance with local policies. In such cases, the prize winners will be required to complete customs clearance procedures as well as cover corresponding taxes incurred.
""", 'EN', 'CHS')
]

def split_content(origin_content, single_input_max_length=1024):
    text_splitter = RecursiveCharacterTextSplitter( 
        chunk_size = single_input_max_length,
        chunk_overlap  = 0,
        separators=["\n\n", "\n", ".", "。", ",","，"," "], 
    )

    chunks = text_splitter.create_documents([ origin_content ] )
    split_chunks = [ chunk.page_content for chunk in chunks ]
    
    return split_chunks

for content, src_lang, dest_lang in content_list:
    chunks = split_content(content)
    print(len(chunks))
