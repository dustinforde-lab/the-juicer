import sqlite3
import os

DB_FILE = "action_grid.db"

def upload_raw_articles():
    print("=" * 65)
    print("📚 [THE LIBRARY] Uploading Raw Unmanipulated Articles...")
    print("=" * 65)
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: {DB_FILE} not found.")
        return

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            
            # Create a dedicated table for raw intelligence
            cur.execute("""
                CREATE TABLE IF NOT EXISTS raw_slate_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Clear previous uploads to prevent duplicates
            cur.execute("DELETE FROM raw_slate_articles")
            
            # Article 1: Cash Game Breakdown
            article_1 = r"""Well, that went well. 
We started off the DFS NFL season with a bang last week, as I saw infinite winning screenshots in Discord and on social media from Elite Mafia members. Both core fours from this article were monstrous hits, so hopefully most of you who used them were able to start out the season well. I do want to remind everybody that most of the time using a QB and RB from the same team won’t result in dual big games as it did with Lamar Jackson and Derrick Henry last week, but we will certainly take it. 
I am pleasantly surprised that there weren’t long lineup trains on FD in week one but am unsure whether that was due to them finding other scams to pull or due to the FanDuel server outages on Sunday morning. My suspicion is the latter, so we need to be prepared to take them on here in week two. If that indeed happens, it would confirm what most of us already know: the lineup trains are an organized band of lonely gypsies who purposely conspire to enter the exact same lineup together on Sunday mornings. I have seen a lot in my day, but these pickle-kissing pillow fuckers are truly a one-of-a-kind breed of dork. 
This week, we have a pretty spread-out field of matchups, none of which quite commands the same attention that the Saints/Lions did last week. I assume the Bears will be popular after their 59-point outing, but outside of Caleb Williams and maybe D’Andre “Julius Pepperwood” Swift, nobody else seems to have interest. Meanwhile, a host of players who were written up in this space last week will be super popular this week because of their success. I expect Jalen Coker, who was 3% owned last week, to be super popular and Lamar Jackson to return to the good graces of DFS players after he showed them that he is again a true two-way threat. 
Thus, we have our work cut out for us this week. It’s much easier getting to the top of the mountain than it is to stay there. But it feels pretty damn good to be on top of this mountain. I kind of like the view. Maybe we will just go ahead and stay here a while. What do you say? 
Here is all our great DFS NFL content for this season: 
Monday – Lineup Review with Patio Joe Baldino
Tuesday – QB Coach with Chris Rose
Wednesday – RB Coach with Ted Schuster
Also Wednesday – Contest Selection with Patio Joe Baldino
Thursday – WR Coach with Tyler Buecher
Friday – TE Coach with Jorge Pucks
Friday x2 – DFS NFL Matchups by Armando Marsal
Also Friday – Cliff’s Notes with Ryan Clifford
More Friday – Cash Game Breakdown (what you are currently reading)
Even More Friday (7pm ET) – Core 4 NFL Livestream hosted by Tyler Buecher
Crazy More Friday (9pm ET) – CFB Livestream hosted by Scott Bondar, Mike the Beard and Chris Rose
Saturday – GPP Writeup with Chris Rose
Also Saturday – DST Coach with Scott Bondar
Saturday DFS NFL Article – DFS Marlin’s Catch of the Week
Sunday – NFL Sunday Livestream hosted by Armando Marsal at 11am ET 
Sunday Kickoff Chat – Lineup lock chat with Ted Schuster at 11:30am ET
Sunday Gameday Chat – All are invited to hang out with me & others in the MANS Cave Discord Room
Here is the DFS NFL Cash Game Breakdown for Week 2
Narrative Street Week 2
By Sandro Anello
Every week, Sandro Anello goes beyond the matchups to uncover all of the motivating factors for each NFL team and player. From birthdays to revenge to contract status and other incentives, there is literally no stone left unturned here this season. 
Birthdays This Week

WED 16 CIN RB Samaje Perine, NE WR Mack Hollins, DAL QB Sam Howell, MIN RB DeeJay Dallas
THU 17 HOU TE Marlin Klein
SAT 19 MIA QB Kyle McCord
MON 21 SF WR Demarcus Robinson
TUES 22 TEN TE Daniel Bellinger
Revenge Matchups

TB QB Baker Mayfield vs. CLE
CHI QB Case Keenum vs. MIN
GB QB Tyrod Taylor vs. NYJ
TEN TE Kylen Granson vs. PHL
DEN TE Evan Engram vs. JAX
LAC WR Gary Jennings vs. LV
DAL QB Sam Howell @ WAS
Hometown Narratives

CAR TE Darren Waller @ ATL
CAR TE Tommy Tremble @ ATL 
MIN QB J.J. McCarthy @ CHI
PIT TE Pat Freiermuth @ NE
GB WR Bo Melton @ NYJ
JAX WR Travis Hunter @ DEN
LV WR Jalen Nailor @ LAC
SEA WR Rashid Shaheed @ ARI
Milestones

LV QB Kirk Cousins 140 passing yards from 45,000
TB QB Baker Mayfield 3 passing TDs from 200
BAL RB Derrick Henry 98 rushing yards from 9th all-time
BAL RB Derrick Henry 18 scrimmage yards from 15,000
BAL RB Derrick Henry 2 total TDs from 8th all-time
SF RB Christian McCaffrey 2 total TDs from 100
CHI RB D’Andre Swift 101 rushing yards from 5,000
WAS WR Stefon Diggs 6 receptions from 22nd all-time
WAS WR Terry McLaurin 25 receiving yards from 7,000
SF WR Mike Evans 98 receiving yards from 19th all-time
SF WR Mike Evans 2 total TDs from 20th all-time
SF WR Deebo Samuel 2 total TDs from 50
SF TE George Kittle 3 receptions from 600
Sandro’s Randos 

BAL QB Lamar Jackson  
With five TD passes, Jackson becomes the fourth quarterback all-time with at least five touchdown passes in seven career games.
CHI QB Caleb Williams
With one TD pass and no more than 2 interceptions. Williams can join Lamar Jackson (10 interceptions) and Patrick Mahomes (13) as the only quarterbacks all-time with 15-or-fewer interceptions at the time of their 50th touchdown pass.
PHL QB Jalen Hurts       
With a rushing & passing TD, Hurts becomes the fifth quarterback all-time with both a touchdown pass and a rushing touchdown in at least 30 career games.
PIT QB Aaron Rodgers
With a win, Rodgers can tie Ben Roethlisberger for the fifth-most regular-season wins in NFL history.
BAL RB Derrick Henry   
With another multiple touchdown game, Henry ties Randy Moss for the fourth-most games with multiple touchdowns in NFL history.
With three rushing TDs, Henry becomes the third player ever with at least six rushing touchdowns in nine consecutive seasons.
With 200 scrimmage yards, Henry becomes the fifth player in NFL history with at least 200 scrimmage yards in 10 career games.
CHI RBs D’Andre Swift & Kyle Monangai
If they both have at least 100 yards rushing, they can join John Cappelletti and Lawrence McCutcheon of the 1976 Los Angeles Rams as the only pair of teammates in NFL history each with at least 100 rushing yards in their team’s first two games of a season.
SF RB Christian McCaffrey
With one receiving TD, McCaffrey surpasses Marshall Faulk for the most touchdown receptions by a running back in the Super Bowl era.
With two total TDs, McCaffrey can surpass Jerry Rice as the fourth-fastest player to reach 100 scrimmage touchdowns in the Super Bowl era.
HOU RB David Montgomery
With at least two touchdowns, Montgomery can become the sixth player ever with at least five scrimmage touchdowns in their first two games with a new team.
MIN WR Justin Jefferson
With 31 receiving yards, Jefferson can surpass DeAndre Hopkins for the second-most receiving yards by a player under the age of 28 in NFL history.
NO WR Chris Olave
With 10 receptions and 100 receiving yards, Olave can become the sixth player in NFL history with at least 10 receptions and 100 receiving yards in each of his team’s first two games of a season.
ARI TE Trey McBride     
With 10 receptions, McBride becomes the fifth tight end in NFL history with at least 10 receptions in 10 career games.
The Bears
With 37 points scored against Minnesota on Sunday, the Bears can surpass the 1968 Oakland Raiders (95 points scored) for the most points scored in a team’s first two games of a season in NFL history.
Can become the first team ever with at least 250 passing yards and 250 rushing yards in consecutive games.
With two rushing touchdowns, the Bears can tie the 1971 Dallas Cowboys (eight rushing touchdowns) and 1961 San Diego Chargers (eight) for the most rushing touchdowns by a team in their first two games of a season since 1932.
WEATHER
Cleveland Browns at Tampa Bay Buccaneers – As of this writing, this is the game with the most likely rain showers during it. They also love to pause play in Tampa Bay, so be aware of that possibility. 
Minnesota Vikings at Chicago Bears – 40% chance of rain showers at Soldier Field. There is a lot of rain expected on Saturday in Chicago, so the field will be soggy and slow. 
Pittsburgh Steelers at New England Patriots – Some rain moving into the area and a 40% chance of a shower during this game. 
New Orleans Saints at Baltimore Ravens – A 30% chance of rain showers in otherwise fine conditions. 
VEGAS

Copy
CSV
ExcelFAV
BUF
DOG
DET
Reset filters
BUFDET54.5-5.530.0024.50——
Updated Sep 18, 7:32 AM ET
QUARTERBACKS
QB TABLE

Copy
CSV
Excel
TEAM
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
OPP
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
Reset filters
Patrick MahomesKCIND4651372.27131.608274.6821.187Caleb WilliamsCHIMIN23199133.15731.4182910.4158.737Jaxson DartNYGLAR8111115112.63933.456298.5576.163Josh AllenBUFDET19184243.11427.92912.61210.538Jayden DanielsWASDAL2261693.41528.745348.6424.908Carson WentzMINCHI7829142.75832.75198.2639.123Jalen HurtsPHITEN952910103.26431.0512510.16210.318Trevor LawrenceJAXDEN10211017162.98136.0242311.21111.169Lamar JacksonBALNO16161714233.30435.5562510.7588.866Joe BurrowCINHOU53126212.54230.151356.8184.519Baker MayfieldTBCLE31721152.88433.1284.692.031Bryce YoungCARATL3027266123.02524.5623710.0428.716Brock PurdySFMIA2017187202.68834.491344.5773.796Tyler ShoughNOBAL27312822172.60223.764568.8378.66Kirk CousinsLVLAC1191630292.89732.13307.6494.141Dak PrescottDALWAS1213825282.74725.837348.263.91Jordan LoveGBNYJ22242728272.56224.6914211.05510.745Cooper RushATLCAR14312182.65331.905224.4871.748C.J. StroudHOUCIN25252223192.78730.082387.8185.992Jared GoffDETBUF13141318252.65931.552396.0334.077Aaron RodgersPITNE141024812.95127.617409.5123.846Cam WardTENPHI1512151952.90324.95325.733.403Jacoby BrissettARISEA21222527222.55832.5377.846.647Kyler MurrayMINCHI782914—32.755——Geno SmithNYJGB18151220133.04236.062246.727.036
«
‹
Page 1 of 2
›
»
Rows per page
10
25
50
100
Updated Sep 15, 9:19 AM ET
WEEK 2 DFS NFL QB BREAKDOWN
Projected Ownership (FanDuel)

1) Dak Prescott, Cowboys – 24% 
2) Drake Maye, Patriots – 16% 
3) Brock Purdy, 49ers – 11% 
4) Jayden Daniels, Commanders – 9%
5) Justin Herbert, Chargers – 8% 
Projected Ownership (DraftKings)

1) Dak Prescott, Cowboys – 22% 
2) Brock Purdy, 49ers – 15% 
3) Jayden Daniels, Commanders – 9%
4) Jordan Love, Packers – 8% 
5) Caleb Williams, Bears – 7% 
Player Pool

Caleb Williams, Bears ($8400/$6800) – If Caleb Williams isn’t the highest or even second-highest QB in DFS this week, then their process is wrong. We are not interested in Caleb because the Bears scored 59 points or because he had the most fantasy points of all QBs last week. We are interested in him because before the season started, Bears head coach Ben Johnson said that he wanted his team to score more points than the 2013 Denver Broncos. Then, with his team up 52-31 late in the fourth quarter last week, he called a designed QB run from the six-yard line, then two pass attempts and a QB sneak from the one-yard line. All to pad the Bears and specifically his QB’s numbers. I strongly doubt that the Bears offense can come anywhere close to that kind of production against Brian Flores’ defense, but the mere fact that an NFL head coach would go to those extremes to ring up the score is something we are going to have to consider often this season. 
Lamar Jackson, Ravens ($8800/$7300) – Lamar is more expensive here but is playing a similar opponent to the one he did last week, this time at home. I loved what we saw from this Baltimore offense last week, and Jackson showed that he is healthy and willing to take off and run with the football again. Whenever Lamar is doing that, he wins MVP of the league. If Zay Flowers doesn’t play, I might reconsider using Lamar in cash games, but that will all come down to what his ownership level is this week. 
Dak Prescott, Cowboys ($8000/$6400) – Dak’s final numbers last week against the Giants weren’t great, but he also had almost no help, as his receivers dropped four passes, ran into each other twice, and committed two penalties against the Giants. This is a sure-fire bounce-back spot for him, as he has always fared well against Dan Quinn’s defenses. Maybe that has something to do with practicing against them every day for three years. I was hoping that Prescott’s ownership would be low this week after that stinker in week one, but that does not look like it will be the case. 
Carson Wentz, Vikings ($7000/$4600) – Put it this way, I am going to consider every single QB against the Chicago Bears defense this season, so Wentz will not be an exception. Now I may not want to go down this path in cash games despite that super low DK price staring me in the face. But with a full week of practice and a trio of premium pass catchers at his disposal, Wentz is one of the better QB options for us in DFS this week. 
Justin Herbert, Chargers ($7400/$6000) – There is nothing sweeter than winning with the player(s) that the majority of the field failed with the previous week. Herbert is an arch enemy of the DFS universe right now after laying a giant egg in what was supposed to be a gimme matchup against the Cardinals last week. Well, the Raiders are an improved defense, but their secondary is young and beatable and something that Mike McDaniel will likely pick on this week. It is not going to feel good plugging Herbert into any of our lineups this week, but the fact that it isn’t easy is why it is a great play. 
Preferred Cash Game (50/50) Plays

1) Caleb Williams, Bears ($8400/$6800)
2) Dak Prescott, Cowboys ($8000/$6400)
3) Lamar Jackson, Ravens ($8800/$7300)
Preferred Single-Entry GPP Plays

1) Caleb Williams, Bears ($8400/$6800)
2) Justin Herbert, Chargers ($7400/$6000)
3) Carson Wentz, Vikings ($7000/$4600)
RUNNING BACKS
RB TABLE

Copy
CSV
Excel
TEAM
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
OPP
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
Reset filters
Bijan RobinsonATLCAR1111212861659.60.000.00Kenneth WalkerKCIND4331318601846.04.002.00Derrick HenryBALNO16174147432141.06.002.00Kyren WilliamsLARNYG6101351451225.04.002.00Jahmyr GibbsDETBUF1367188621447.28.005.00Bhayshul TutenJAXDEN1022171618130.20.000.00Jordan MasonMINCHI712891131926.34.001.00Emmett JohnsonKCIND4331318——15.91.000.00Aaron Jones Sr.MINCHI712891112522.84.001.00Javonte WilliamsDALWAS128272510541335.45.003.00Jacory Croskey-MerrittWASDAL2119162235727.91.001.00Cam SkatteboNYGLAR8419151722427.34.002.00Devin SingletaryNYGLAR8419151717215.23.000.00Brian RobinsonATLCAR111121222417.30.000.00Blake CorumLARNYG6101351251017.90.000.00Christian McCaffreySFMIA2024572471128.12.000.00Ameer AbdullahJAXDEN10221716409.40.000.00Ashton JeantyLVLAC111418303061543.97.000.00Bucky IrvingTBCLE31822212330431.92.000.00Saquon BarkleyPHITEN915121013531336.22.000.00Ronnie RiversLARNYG61013511010.72.000.00Travis Etienne Jr.NOBAL27510222746923.43.000.00Breece HallNYJGB1819172021401738.74.002.00Rachaad WhiteWASDAL2119162225414.82.000.00David MontgomeryHOUCIN252216231929633.36.003.00
«
‹
Page 1 of 5
›
»
Rows per page
10
25
50
100
Updated Sep 15, 9:19 AM ET
OFFENSIVE LINE/DEFENSIVE LINE SMASH REPORT WEEK 2


Copy
CSV
Excel
Arizona25.5637.89Atlanta29.4737.32Baltimore41.3325.98Buffalo60.8532.50Carolina51.5818.93Chicago75.4611.76Cincinnati27.6028.32Cleveland43.6026.30Dallas41.1124.56Denver37.3938.06Detroit55.8637.79Green Bay16.3525.08Houston40.0254.91Indianapolis34.6511.36Jacksonville57.1923.02Kansas City54.8343.80Las Vegas66.0638.75LA Chargers25.0327.64LA Rams46.5538.07Miami14.0910.70Minnesota37.1349.99New England31.0922.09New Orleans56.2228.43NY Giants57.7819.22NY Jets53.2532.46Philadelphia50.0646.92Pittsburgh30.7453.69San Francisco68.8429.81Seattle39.2650.80Tampa Bay61.5323.21Tennessee21.7714.52Washington22.3212.00
Updated Sep 17, 1:12 PM ET
SMASH MATCHUP REPORT WEEK 2


Copy
CSV
Excel
DET55.8637.7923.36423.05560.8532.50BUFCAR51.5818.9314.26710.54029.4737.32ATLMIN37.1349.9925.37425.47175.4611.76CHIPHI50.0646.9235.540-25.14721.7714.52TENPIT30.7453.698.655-22.60331.0922.09NEGB16.3525.08-16.11628.17353.2532.46NYJCLE43.6026.3020.39835.23161.5323.21TBNO56.2228.4330.24112.90241.3325.98BALCIN27.6028.32-27.31111.69940.0254.91HOUJAC57.1923.0219.12614.36937.3938.06DENLVR66.0638.7538.419-13.71825.0327.64LACWAS22.3212.00-2.24329.11241.1124.56DALSEA39.2650.801.373-25.24825.5637.89ARIMIA14.0910.70-15.72258.13868.8429.81SFIND34.6511.36-9.14943.47654.8343.80KCNYG57.7819.2219.71727.32946.5538.07LAR
Updated Sep 17, 1:39 PM ET
O-LINE/D-LINE MATCHUPS
(Mans’ Model – Point System Scale of -100 – 100)
Main Slate Games Only
1) San Francisco 49ers ➡️ Miami Dolphins – +58.13
2) Las Vegas Raiders ➡️ Los Angeles Chargers – +38.41
3) Philadelphia Eagles ➡️ Tennessee Titans – +35.54
4) Tampa Bay Buccaneers ➡️ Cleveland Browns – +35.23
5) New Orleans Saints ➡️ Baltimore Ravens – +30.24
6) Dallas Cowboys ➡️ Washington Commanders – +29.11
WEEK 2 DFS NFL RB BREAKDOWN
Projected Ownership (FanDuel)

1) Bijan Robinson, Falcons – 45% 
2) Javonte Williams, Cowboys – 34%
3) Derrick Henry, Ravens – 33% 
4) Christian McCaffrey, 49ers – 31% 
5) Aaron Jones, Vikings – 29% 
Projected Ownership (DraftKings)

1) Bijan Robinson, Falcons – 42% 
2) Javonte Williams, Cowboys – 38%
3) Aaron Jones, Vikings – 29%
4) Derrick Henry, Ravens – 26% 
5) Christian McCaffrey, 49ers – 26%
Player Pool

Bijan Robinson, Falcons ($8900/$8200) – Bijan is the RB who most players will pay up for, and that is perfectly understandable, coming off a monstrous 29-touch, 173-yard performance in week one. The Panthers got their shit pushed in by the Chicago offensive line last week, but I do not think this is a bad run defense at all. Bijan will be the backbone of the Falcons offense again and will likely see 25+ touches as well. 
De’Von Achane, Dolphins ($8200/$6700) – This is a real sneaky play because Achane is coming off of a disappointing effort last week against the Raiders. But the truth of the matter is that Vegas is a much better run defense this year, while the 49ers are quite poor. Remember that the Rams were shredding San Francisco on the ground before LA had to shift into catch-up mode and throw most of the second half. The great thing about Achane is that he will also be among the Dolphins’ leading pass catchers, giving him double the opportunities to break off big runs. Achane’s price on DK is so good that he deserves strong consideration for our core four over there this week. 
Aaron Jones, Vikings ($5900/$5100) – The majority of DFS lineup builds will include one super high-priced RB, likely Bijan Robinson, paired with the Vikings Aaron Jones. Jordan Mason is out for the next few weeks, leaving Jones as the Vikings’ new feature RB going forward. Jones has always produced against the Bears. He has scored 14 touchdowns against Chicago and averages 16.3 fantasy points per game against them throughout his career. 
Javonte Williams, Cowboys ($7400/$6400) – Like Dak Prescott, Javonte Williams will also be a popular name this week due to the high expected total and game script. Similar to Judkins, Javonte has nobody else splitting time with him and thus will accumulate the vast majority of touches, targets, yards, goal-line touches and fantasy points among the Cowboys backfield. He is severely underpriced, which will result in a high ownership number for sure. 
Christian McCaffrey, 49ers ($9000/$8000) – You know that it is a brand-new season when a modestly priced CMC going against the worst defense in the NFL is not expected to generate a lot of DFS ownership. That is because everybody is reading into Kaelon Black’s usage in week one as the new status quo in San Francisco. It isn’t. McCaffrey was dealing with cramps in an extremely hot outback against the Rams and has had 11 days to hydrate. This is the kind of game that CMC goes for 30+ and becomes the darling of the fantasy football world again. 
Quinshon Judkins, Browns ($6000/$5400) – Judkins is one of maybe four running backs in the entire NFL who will claim over an 80% stake of his team’s backfield this week (and into the future). Now that Dylan Sampson is out for the season, Judkins will get even more passing-down work, which helps keep him game-script agnostic. Despite having a beast like Vita Vea in the middle of their defense, the Bucs are seventh worst in DVOA against the run. He is a nice, safe, cheap option that nobody else will use because he lacks the support of most projection model systems. 
Chuba Hubbard, Panthers ($6300/$5800) – Evidently, Jonathon Brooks is still nowhere near ready to take on a significant role in the Panthers offense, leaving the majority share to Hubbard. Chuba was 11th among RBs in snap share last week and draws a much better game script this week against the Falcons, who are struggling to stop the run. I really don’t like the value options at running back this week, and Chuba is really underpriced on both sites for what his role is right now.  
Preferred Cash Game (50/50) Plays

1) Bijan Robinson, Falcons ($8900/$8200)
2) Javonte Williams, Cowboys ($7400/$6400)
3) Aaron Jones, Vikings ($5900/$5100)
4) De’Von Achane, Dolphins ($8200/$6700)
Preferred Single-Entry GPP Plays

1) De’Von Achane, Dolphins ($8200/$6700)
2) Christian McCaffrey, 49ers ($9000/$8000)
3) Quinshon Judkins, Browns ($6000/$5400)
4) Chuba Hubbard, Panthers ($6300/$5800)
WIDE RECEIVERS
WR TABLE

Copy
CSV
Excel
TEAM
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
OPP
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
Reset filters
Justin JeffersonMINCHI7851339.146.39.3688.92.993.47Antonio WilliamsWASDAL2226113.8——100.0—4.10Stefon DiggsWASDAL2226131.033.09.1944.42.541.72Rashee RiceKCIND46858.0——100.0—4.95Emeka EgbukaTBCLE3132122.265.213.7583.32.401.88Dontayvion WicksPHITEN9516718.2——50.0—3.83Chris Godwin Jr.TBCLE3132114.8——100.0—2.08CeeDee LambDALWAS121319326.735.911.5062.53.041.93Puka NacuaLARNYG67151633.345.211.9655.61.621.38Zay FlowersBALNO1616102025.031.313.4683.32.454.33Tee HigginsCINHOU5362517.648.918.8950.01.811.48Ted Hurst IIITBCLE3132111.1——100.0—2.20DeVonta SmithPHITEN9516727.337.313.8850.02.561.38Kalif RaymondCHIMIN231921434.623.16.9688.93.701.82Amon-Ra St. BrownDETBUF131491535.930.15.0671.43.612.05Xavier WorthyKCIND468524.040.77.9450.04.150.80Malik NabersNYGLAR81143231.040.211.0866.72.841.43Christian WatsonGBNYJ222421420.027.815.3575.02.494.09Drake LondonATLCAR1471723.838.07.1640.04.541.10Jaxon Smith-NjigbaSEAARI282317745.854.57.2872.73.092.38DJ MooreBUFDET191812228.644.019.4062.52.802.63Jack BechLVLAC119142413.8——75.0—2.83Luther Burden IIICHIMIN231921419.213.17.11100.02.801.90Deebo Samuel Sr.SFMIA2017241220.611.42.5385.74.722.57Mike EvansSFMIA2017241220.640.08.9085.71.952.41
«
‹
Page 1 of 8
›
»
Rows per page
10
25
50
100
Updated Sep 15, 9:19 AM ET
WB/CB MATCHUPS
WB/CB MATCHUPS (BASED ON PFF RATINGS)
Main Slate Games Only
1) Jaxon Smith-Njigba, Seahawks ➡️Will Johnson, Cardinals 
2) Zay Flowers, Ravens ➡️ Quincy Riley, Saints 
3) Justin Jefferson, Vikings ➡️ Jaylon Johnson, Bears 
4) Jalen Coker, Panthers ➡️ Sydney Brown, Falcons 
5) Christian Watson, Packers ➡️ Brandon Stephens, Jets 
6) Cooper Kupp, Seahawks ➡️ Denzel Burke, Cardinals 
7) Mike Evans, 49ers ➡️ Jason Marshall Jr, Dolphins 
8) Deebo Samuel, 49ers ➡️ Chris Johnson, Dolphins
9) Parker Washington, Jaguars ➡️ Riley Moss, Broncos
10) Ladd McConkey, Chargers ➡️ Darien Porter, Raiders 
11) Chris Olave, Saints ➡️ Marlon Humphrey, Ravens
12) Caleb Douglas, Dolphins ➡️ Renardo Green, 49ers 
WORST COVERAGE CORNERBACKS – WR MATCHUP (Mans Model)

SMASH COVERAGE MATCHUPS WEEK 2 (MAIN SLATE) RANKDEFENSIVE BACKTEAMCOVERAGE TYPEADVPRIMARY RECEIVERTEAM1Tyrique StevensonCHI45% Cover-1 Man70.63Justin JeffersonMIN2Jason MarshallMIA45% Cover-3 Zone66.94Mike EvansSF3Mike SainristilWAS85% Match Zone64.57Ryan FlournoyDAL4Jarvin BrownleeNYJ50% Cover-2 Zone57.81Jayden ReedGB5Upton StoutSF65% Cover-6 Zone50.02Malik WashingtonMIA6Benjamin MorrisonTB50% Cover-3 Zone46.46Denzel BostonCLE7Quincy RileyNO60% Cover-3 Zone45.93Devontez WalkerBAL8Amik RobertsonWAS85% Match Zone40.22George PickensDAL9Malik MuhammadCHI45% Cover-1 Man38.59Myles PriceMIN10Brandon CisseGB45% Cover-2 Zone35.36Garrett WilsonNYJ11Myles HardenCLE55% Cover-3 Zone32.79Chris GodwinTB12Billy BowmanATL50% Cover-2 Zone30.84Jalen CokerCAR13Cam HartLAC40% Cover-4 Zone28.32Tre TuckerLVR14Eric StokesLVR50% Cover-3 Zone26.50Quentin JohnstonLAC15Dax HillCIN50% Man Coverage25.09Kayshon BoutteHOU16Azareye’h ThomasNYJ50% Cover-2 Zone23.77Matthew GoldenGB17Cordale FlottTEN45% Cover-4 Zone20.46Dontayvion WicksPHI18Denzel BurkeARI45% Cover-6 Zone19.42Jaxon Smith-NjigbaSEA19Jamel DeanPIT50% Cover-4 Zone18.32Romeo DoubsNE20Montaric BrownJAC55% Cover-4 Quarters16.59Pat BryantDEN21Chris JohnsonMIA45% Cover-3 Zone15.78Deebo SamuelSF22Chau Smith-WadeCAR50% Cover-3 Zone13.39Zachariah BranchATL23Donte JacksonLAC40% Cover-4 Zone12.66Jalen NailorLVR24Ja’Quan McMillanDEN55% Cover-1 Man10.15Parker WashingtonJAC25Byron MurphyMIN65% Match Zone8.98Luther BurdenCHI
WEEK 2 DFS NFL WR BREAKDOWN
Projected Ownership (FanDuel)

1) Quentin Johnson, Chargers – 29%
2) Terry McLaurin, Commanders – 25% 
3) Luther Burden, Bears – 24% 
4) CeeDee Lamb, Cowboys – 22% 
5) Garrett Wilson, Jets – 21% 
6) Matthew Golden, Packers – 16% 
Projected Ownership (DraftKings)

1) CeeDee Lamb, Cowboys – 24% 
2) George Pickens, Cowboys – 22% 
3) Garrett Wilson, Jets – 21% 
4) Ja’Marr Chase, Bengals – 20% 
5) Rashod Bateman, Ravens – 18% 
6) Matthew Golden, Packers – 15% 
Player Pool

Justin Jefferson, Vikings ($8600/$7800) – Jefferson is by far the best overall wide receiver on the slate. The Bears secondary is tragically poor, and J-Jetta reminded us last week that he is still indeed one of the best receivers in the league. Carson Wentz may not be a premium QB any longer, but he knew well enough last week that throwing to Jefferson was the best way to move this Minnesota offense, and it worked out extremely well to the tune of a 9-8-92-2 stat line. If you pay up for WR, this is your guy. Period. 
Luther Burden, Bears ($6000/$5700) | Rome Odunze, Bears ($6300/$5500) – Yeah, we are going to attack this game despite the rain in the forecast. It seems as though everybody is downgrading the Bears receivers for no reason whatsoever, despite everybody also talking about their desire to break every offensive record ever created. I will leave it up to you which Bears WR to use this week because they are both very, very good plays at these price points. For me, I think that Burden makes for a better cash game play, given his higher baseline, and Odunze is a better GPP play because of his big-play ability.
George Pickens, Cowboys ($8000/$6300) – We could put both Cowboys WRs in this space as well, but I won’t take the easy way out. Of course Lamb is in play if you had the money, but I believe the best lineup build this week is paying up for the RBs and down for the WRs. If you did use some value options elsewhere, then it is possible to squeeze in Pickens, but I believe that Lamb is priced just a bit beyond our capabilities. Pickens needs to concentrate better this week and make the catches that he dropped last week against the Giants, and if he can do that, his numbers will be very good for us in DFS. 
Garrett Wilson, Jets ($7200/$6000) – Wilson started the season strong by dropping a modest 13.9 fantasy point total against the Titans last week. What’s better is that he showed great chemistry with Jets QB Geno Smith, which is the only thing that can hold this talented receiver down. Well, that and injuries like last year, but I digress. The Jets are undoubtedly salivating at the thought of Wilson taking on Packers rookie CB Brandon Cisse this week, which should lead to a bounty of targets. 
Denzel Boston, Browns ($4700/$4200) – Before the season, we had no idea how this Browns receiving corps would play out. We got a good idea in week one, where Boston played 92.2% of snaps, which was the eighth-highest among WRs in the NFL last week. He only generated four targets, though, and caught just two of them against the Jaguars in a blowout loss. But one of those catches was a 46-yard TD that demonstrated his ability to get loose deep and make plays on the football that few others can. We are going to target against the Buccaneers’ coverage a lot this season but few will have the guts to do it with the Browns here in week two. 
Romeo Doubs, Patriots ($5800/$5000) – It is so funny how fickle fantasy players can be. Normally, if A.J. Brown was put in IR, the next man up in the offense would be a prime target. Yet Doubs, who the Patriots signed to a four-year, $68 million contract with $39 million guaranteed this offseason, was DROPPED more than he was added to seasonal fantasy rosters this week. Nobody is using him in DFS this week either, which is peculiar since the Steelers are also without their top CB, Joey Porter Jr. 
Matthew Golden, Packers ($5900/$4700) – Golden played in all two-WR sets last week and demonstrated great strides in both getting open and running after the catch. He received 12 targets, which has fantasy players salivating at the prospect of him doing that every week (he won’t). This is clearly a WR who will be priced up toward the $7K range soon, so we are getting an outstanding value for him here this week. 
Kayshon Boutte, Texans ($5200/$4000) – Boutte played far less than I thought he would last week, with just 45.6% of snaps and seeing just 5% of targets. But now that Nico Collins is out for the Texans, Boutte steps into the leading man role here for CJ Stroud and the Houston passing offense. Others will guess that Xavier Hutchinson or Jaylin Noel will be the one to step up, but the player who most resembles Nico Collins’ skill set and strengths is Boutte. 
Wan’Dale Robinson, Titans ($5300/$4600) – I could probably just etch Duke Silver’s name into the Cash Game Breakdown every week because he will usually outproduce his price tag in DFS. Robinson has extensive experience against the Eagles and has fared well against them over his career with the Giants, averaging six catches and 51 yards per game against them. The Titans will likely be in a pass-heavy script here, allowing Wan’Dale to meet or exceed those averages this week. 
DK Value Plays

DeMario Douglas, Patriots – $3800
Kalif Raymond, Bears – $3600
DeVontez “Tez” Walker, Ravens – $3400
Preferred Cash Game (50/50) Plays

1) Justin Jefferson, Vikings ($8600/$7800)
2) Luther Burden, Bears ($6000/$5700)
3) Garrett Wilson, Jets ($7200/$6000)
4) Romeo Doubs, Patriots ($5800/$5000)
5) Matthew Golden, Packers ($5900/$4700)
6) Wan’Dale Robinson, Titans ($5300/$4600)
Preferred Single-Entry GPP Plays

1) Rome Odunze, Bears ($6300/$5500)
2) George Pickens, Cowboys ($8000/$6300)
3) Kayshon Boutte, Texans ($5200/$4000)
4) Denzel Boston, Browns ($4700/$4200)
5) Matthew Golden, Packers ($5900/$4700)
6) Justin Jefferson, Vikings ($8600/$7800)
TIGHT ENDS
TE TABLE

Copy
CSV
Excel
TEAM
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
OPP
ARI
ATL
BAL
BUF
CAR
CHI
CIN
CLE
DAL
DEN
DET
GB
HOU
IND
JAX
KC
LAC
LAR
LV
MIA
MIN
NE
NO
NYG
NYJ
PHI
PIT
SEA
SF
TB
TEN
WAS
Reset filters
Mike GesickiCINHOU5678.420.630.310.0471.42.622.69Chig OkonkwoWASDAL2146.010.3——66.7—1.20Dallas GoedertPHITEN91248.522.723.810.6680.03.214.74John BatesWASDAL2112.010.3——66.7—1.10Michael MayerLVLAC11423.324.113.04.1285.72.801.31Drew SampleCINHOU568.18.8——100.0—1.63Travis KelceKCIND41642.120.024.85.8160.02.852.02T.J. HockensonMINCHI71839.821.713.74.9980.02.812.72Brenton StrangeJAXDEN101436.214.3——66.7—3.43Kenyon SadiqNYJGB188—13.0——100.0—3.80Isaiah LikelyNYGLAR82573.227.627.18.42100.03.043.48Cade OttonTBCLE31848.618.519.14.8560.04.061.12Trey McBrideARISEA211562.835.132.77.3069.22.791.89Dalton KincaidBUFDET19254.321.426.715.7383.32.003.00Harold Fannin Jr.CLETB17341.413.6——66.7—1.37Brevyn Spann-FordDALWAS12524.36.7——100.0—1.70Cole KmetCHIMIN231018.911.5——66.7—3.83Jake FergusonDALWAS12554.26.7——100.0—1.30Josh OliverMINCHI71813.917.4——50.0—1.05Luke SchoonmakerDALWAS12521.93.3——100.0—2.20Blake WhiteheartCLETB17328.04.5——100.0—2.40Tanner HudsonCINHOU5646.62.9——100.0—1.40Mark AndrewsBALNO162069.225.016.47.0766.73.261.48Jake BriningstoolKCIND416—4.0——100.0—1.90Sam LaPortaDETBUF131340.420.514.34.2162.54.051.23
«
‹
Page 1 of 5
›
»
Rows per page
10
25
50
100
Updated Sep 15, 9:19 AM ET
WEEK 2 DFS NFL TE BREAKDOWN
Projected Ownership (FanDuel)

1) Mark Andrews, Ravens – 39% 
2) Dalton Schultz, Texans – 19%
3) Colston Loveland, Bears – 17% 
4) Michael Mayer, Raiders – 14%
5) Trey McBride, Cardinals – 8% 
Projected Ownership (DraftKings)

1) Mark Andrews, Ravens – 33% 
2) Dalton Schultz, Texans – 28% 
3) Michael Mayer, Raiders – 25% 
4) Colston Loveland, Bears – 10% 
5) George Kittle, 49ers – 8% 
Player Pool

Mark Andrews, Ravens ($5200/$4400) – The TE position is pretty mediocre this week, and you will notice that just about every player in my pool is about the same price on FanDuel, which absolutely sucks. The Ravens are banged up at the receiver position, which will give their tight ends a few more targets right off the top. The Saints lost Demario Davis – their best TE stopper – this offseason, leaving a major hole that the rest of the defense isn’t ready to fill. 
Michael Mayer, Raiders ($5300/$3600) – This is assuming Brock Bowers misses another game, which I would be stunned if he didn’t. Mayer showed very well last week even though it only accounted for 32 yards. The Chargers surrendered the second-most targets and the most receptions to TEs last week and provide a very beatable matchup for Mayer this week. Kirk Cousins is older and doesn’t throw the deep ball much anymore, which is why we were so excited about Bowers going into the season. Mayer’s DK price is ridiculous, considering he was the highest-owned TE on their site last week. 
Luke Farrell, 49ers ($4400/$2500) – He’s not going to rack up many points; let’s just understand that first and foremost. We are hoping for 2-4 catches, 25-35 yards and as good of a chance at scoring a TD as all but seven tight ends in this slate. But here is the case. The 49ers are two TD favorites at home against the Dolphins. Starting TE George Kittle is coming off a torn Achilles and played just 30 snaps in week one in a divisional game against the Rams. Backup TE Jake Tonges suffered a torn MCL and is out for the season. That leaves Farrell as the 49ers’ primary TE, as he was after Tonges got hurt last week. Farrell was 20th in the league among TEs with 70.6% of snaps last week, though he only generated a 2-2-19-0 stat line out of it. The equation here in using Farrell is whether the amount that you save (about $1000 on either site) can be used to upgrade another position enough so that the added point total plus Farrell’s non-TD total is greater than the mid-tier RB-WR and chalk TE combined total. 
Kyle Pitts, Falcons ($5200/$4500) – Save your breath. I know you don’t like it. I know that you “can’t trust him” or “don’t like the Falcons offense” right now. That is why Pitts may wind up as my priority TE this week. The fact that the Falcons QBs stink and that they have no viable receivers other than Drake London, who defenses are building a wall around, will lead to premium production by the newly minted Kyle Pitts. He’ll be under 10% owned in every contest, yet his baseline ownership projection for this game before last week’s stinker was 22%.
T.J. Hockenson, Vikings ($5100/$3500) – Hockenson passed the eye test for me last week, looking faster and stronger than he has since he was traded to the Vikings. Both Kyler Murray and Carson Wentz are notorious TE lovers who love targeting their checkdown options. The Bears will have their hands full with trying to slow down Justin Jefferson, so expect extreme deep coverages, leaving the underbelly of the defense wide open for Hockenson to work. 
Pat Freiermuth, Steelers ($5100/$3700) – It appears as though Mike McCarthy is going to have Freiermuth as the Steelers primary move tight end, as evidenced by him running 31 routes on his 36 snaps in week one. Since Aaron Rodgers cannot push the ball downfield, the RBs and TEs are going to feast on all of those low aDOT targets this season. It’s not a particularly great “matchup” against the Patriots, but this high volume in the snap and route department is going to consistently keep Freiermuth among the TE leaders in games where the Steelers are forced to throw a lot. 
Preferred Cash Game (50/50) Plays

1) Luke Farrell, 49ers ($4400/$2500)
2) Mark Andrews, Ravens ($5200/$4400)
3) Michael Mayer, Raiders ($5300/$3600)
Preferred Single-Entry GPP Plays

1) Kyle Pitts, Falcons ($5200/$4500)
2) Pat Freiermuth, Steelers ($5100/$3700)
3) T.J. Hockenson, Vikings ($5100/$3500)
DEFENSE/SPECIAL TEAMS
Philadelphia Eagles ($4800/$3700)
Baltimore Ravens ($4600/$3300) 
Houston Texans ($4000/$3000)
Carolina Panthers ($3300/$2700)
New York Jets ($3100/$2400) 
WEEK 2 CASH GAME CORE 4’S
FANDUEL CORE 4

QB – Caleb Williams, Bears – $8400
RB – Javonte Williams, Cowboys – $7400
WR – Luther Burden, Bears – $6000
TE – Luke Farrell, 49ers – 4400 
DRAFTKINGS CORE 4

QB – Caleb Williams, Bears – $6800
RB – De’Von Achane, Dolphins – $6700
WR – Luther Burden, Bears – $5700
TE – Luke Farrell, 49ers – $2500
WEEK 2 SINGLE-ENTRY GPP CORE 4’S
FANDUEL CORE 4

QB – Will reveal in Sunday morning update
RB – Will reveal in Sunday morning update
WR – Will reveal in Sunday morning update
TE – Will reveal in Sunday morning update
DRAFTKINGS CORE 4

QB – Will reveal in Sunday morning update
RB – Will reveal in Sunday morning update
WR – Will reveal in Sunday morning update
TE – Will reveal in Sunday morning update"""
            
            # Article 2: Injury Report
            article_2 = r"""Here’s a look at the Week 2 NFL Injury Report ahead of the rest of the games on both sides of the ball. The Lions and Bills have already played. More news will be updated throughout the rest of the weekend, so make sure you check back in on this article. The Giants and Rams play on Monday.
Quarterbacks
Atlanta Falcons QB Tua Tagovailoa (Oblique) is doubtful to face the Panthers in Week 2, and QB Michael Penix Jr. (Knee) is out. QB Cooper Rush, who was dealing with back pain last week, will draw the start against Carolina, with QB Jack Strand backing him up. Rush got picked off twice in Week 1 against the Steelers.
Cincinnati Bengals QB Joe Burrow (Back) is listed as questionable to face the Texans on Sunday, but Coach Taylor made comments that he should be on the field for the game. QB Joe Flacco is Burrow’s backup. 
Las Vegas Raiders QB Aidan O’Connell (Personal) is questionable to face the Chargers after missing his last two practices. QB Kirk Cousins is starting, and QB Fernando Mendoza is his backup. 
Minnesota Vikings QB Kyler Murray (Concussion) didn’t clear the league’s protocol and is out for Week 2 against the Bears. QB Carson Wentz will get the start, and last week against the Packers, he threw 3 TD passes, with two of them going to Justin Jefferson. The Bears allowed Carolina to score 37 points against them. QB J.J. McCarthy will back up Wentz.
Seattle Seahawks QB Sam Darnold (Glute) is out for Week 2 after hurting himself in Week 1. QB Drew Lock will get the start against Arizona, and last week, he threw for 187 yards and a TD. 
Running Backs/Fullbacks
Denver Broncos RB RJ Harvey (Hamstring) has been limited in his last two practices and is questionable to face the Jaguars on Sunday. Harvey played more snaps than RB J.K. Dobbins against the Chiefs in Week 1, but Dobbins was given more carries. If Harvey sits, RB Jonah Coleman and RB Adam Prentice will back up Dobbins. Harvey was also thrown to four times in Week 1. 
Indianapolis Colts RB DJ Giddens (Knee) is questionable to face the Chiefs Sunday night despite fully practicing on Friday. If he’s out, RB Seth McGowan should see more field time in the offense behind RB Jonathan Taylor.
New York Jets RB Kene Nwangwu (Back) missed practice all week and is out against the Packers on Sunday. 
San Francisco 49ers RB Kaelon Black (Groin) has been limited in his last couple of practices and is questionable to face Miami on Sunday. Black was a very popular pickup on the waiver wire this week after getting a bunch of work in Week 1 with a healthy RB Christian McCaffrey. If Black sits, the 49ers can opt for RB Jordan James to potentially back up McCaffrey on Sunday in a game where the 49ers should easily take care of Miami. 
Wide Receivers
Baltimore Ravens WR Zay Flowers (Hamstring) is doubtful to face the Saints on Sunday. If he joins WR Ja’Kobi Lane on the shelf, we should see WR Rashod Bateman and TE Mark Andrews pick up targets, and WR Chris Moore should be in the mix a bit more. Andrews was targeted six times last week by QB Lamar Jackson.
Denver Broncos WR Marvin Mims (Foot) is out for Week 2 against the Jaguars after not practicing all week. WR Pat Bryant and WR Troy Franklin will see the field more. Bryant led the Broncos in targets in Week 1.
Houston Texans WR Nico Collins (Hamstring) injured his hamstring earlier this week and will be out for Week 2 against the Bengals. WR Xavier Hutchinson, WR Kayshon Boutte and TE Dalton Schultz will pick up a few targets, and the Texans will be forced to throw a ton against a high-octane Bengals offense.
Indianapolis Colts WR Ashton Dulin (Ankle) is out for Week 2 against the Chiefs. WR Laquon Treadwell will be on the field a bit more on Sunday. Unless we find out that WR Alec Pierce has restrictions with his playing time, he’ll be the prioritized pass catcher. 
Los Angeles Chargers WR Ladd McConkey (Ribs) returned to practice on Friday, logging a limited session, and he’s questionable for Sunday against the Raiders. If McConkey sits, WR Quentin Johnston and WR Tre’ Harris will be prioritized more, and the Chargers could once again throw a few passes to TE David Njoku. 
Minnesota Vikings WR Jauan Jennings (Personal) will miss Sunday’s game against the Bears. WR Tai Felton and WR Myles Price should see the field a bit more. 
New Orleans Saints WR Chris Olave (Hamstring) has been limited in practice over the last couple of days, and he’s questionable to face the Ravens on Sunday. If he sits, WR Devaughn Vele and WR Bryce Lance will be the prioritized pass catchers along with TE Juwan Johnson. With RB Alvin Kamara active, QB Tyler Shough can hit him short against the tough Ravens defense.
New York Jets WR Omar Cooper (Ankle) injured himself in Week 1 and won’t play against Green Bay on Sunday. WR Isaiah Williams should be on the field a bit more. 
Pittsburgh Steelers WR Michael Pittman Jr. (Foot) missed the last couple of practices for the week, and he’s questionable to play against New England on Sunday. Beyond WR DK Metcalf, WR Roman Wilson should get a handful of targets, and QB Aaron Rodgers could throw to his RBs (11 targets combined in Week 1) a bunch as well.
San Francisco 49ers WR De’Zhaun Stribling (Ankle) didn’t practice all week and will be sidelined against the Dolphins on Sunday. Stribling being out puts WR Deebo Samuel and WR Demarcus Robinson on the field more. Both Samuel and Robinson scored in Week 1, and Samuel caught six passes. 
Tampa Bay Buccaneers WR Jalen McMillan (Knee) is questionable despite practicing fully all week. If he sits versus the Browns, WR Chris Godwin and TE Cade Otton should be fed a few more targets. Jaguars QB Trevor Lawrence tore the Browns’ defense apart last week. If McMillan sits out again, WR Ted Hurst could take the field more.
Tight Ends
Las Vegas Raiders TE Brock Bowers (Knee) is listed as doubtful to face the Chargers on Sunday after returning to practice on Friday. He was limited in the session after missing Week 1. If he sits again, TE Michael Mayer, who just got a contract extension, will pick up a good handful of targets. Mayer led the Raiders in targets in Week 1. 
Washington Commanders TE Chig Okonkwo (Hamstring) is out for Week 2 against Dallas, and TE John Bates should see more of the field. He was targeted three times last week by QB Jayden Daniels against Philadelphia. 
Kickers/Punters
San Francisco 49ers K Eddy Pineiro (Illness) hasn’t practiced all week and is questionable to play against Miami on Sunday. The 49ers don’t have a backup kicker at the moment, so we’ll have to watch the news and see who they sign if Pineiro isn’t ready in time. 
Offensive Linemen
Arizona Cardinals OG Isaiah Adams (Knee) and OG Isaac Seumalo (Shoulder) haven’t been fully practicing and are questionable to face Seattle on Sunday.
Atlanta Falcons OG Chris Lindstrom (Concussion) is still working his way through the league’s protocol, and he’s questionable to battle the Panthers. 
Baltimore Ravens OG John Simpson (Groin) and OT Ronnie Stanley (Toe) are questionable to play Sunday against the Saints after being limited in Friday’s practice.
Cleveland Browns OG Teven Jenkins (Back) missed practice all week and is out for Week 2 against Tampa Bay. 
Green Bay Packers OG Aaron Banks (Knee) and OT Zach Bako-Bewele (Knee) have been limited in practice all week and are questionable to battle the Jets.
Houston Texans OG Ed Ingram (Groin) is out for Week 2 against the Bengals. 
Kansas City Chiefs OT Josh Simmons (Back) missed practice all week and is out for Sunday night’s game against the Colts. 
Los Angeles Chargers OG Trey Pipkins (Knee) is out for Week 2 against Las Vegas.
Miami Dolphins C Tucker Addington (Shoulder) is questionable to face the 49ers in Week 2 after being limited in practice all week. 
Minnesota Vikings OT Brian O’Neill (Knee) returned to practice on Friday on a limited basis, and he’s questionable to battle Chicago on Sunday. 
New England Patriots OT Dametrious Crownover (Knee) is out for Week 2, and C Ben Brown (Knee) is questionable to face the Steelers.
New Orleans Saints C Zach Wood (Calf) will miss Week 2 against the Ravens.
Pittsburgh Steelers OT Troy Fautanu (Ankle) is questionable to face the Patriots on Sunday. 
Seattle Seahawks OG Anthony Bradford (Knee) is questionable to face the Cardinals after missing practice on Friday. 
Defensive Linemen
Arizona Cardinals DT Andrew Billings (Knee) and DT Roy Lopez (Groin) are questionable to face the Seahawks on Sunday. 
Baltimore Ravens DT Nnamdi Madubuike (Neck) won’t play on Sunday against the Saints. 
Carolina Panthers DT Bobby Brown (Back) missed practice all week and will be inactive on Sunday against the Falcons.
Cincinnati Bengals DT B.J. Hill (Achilles) is questionable to face the Texans on Sunday. 
Green Bay Packers DT Warren Brinson (Calf) is out for Week 2, and DT Javon Hargrave (Concussion) is doubtful to face the Jets on Sunday. 
Houston Texans DE Jadeveon Clowney (Knee) hasn’t been practicing, and he’s out for Week 2 against Cincinnati. 
Kansas City Chiefs DT Chris Jones (Calf) was limited in practice all week, and he’s questionable to face the Colts in Week 2. 
Miami Dolphins DE Chop Robinson (Concussion) is out for Week 2 against the 49ers. 
New Orleans Saints DT Christen Miller (Toe) was limited in Friday’s practice, and he’s questionable to face Baltimore on Sunday.
New York Jets DE Joseph Ossai (Foot) is out, and DE Will McDonald (Ankle) has been limited in practice and is questionable to face the Packers.
Washington Commanders DT Javon Kinlaw (Back) was limited in Friday’s practice, and he’s questionable to face Dallas.
Linebackers
Baltimore Ravens LB Teddye Buchanan (Knee) won’t play Sunday. LB Trey Hendrickson (Finger) was limited in Friday’s practice, and he’s questionable to face the Saints. 
Carolina Panthers LB Patrick Jones (Back) logged two limited practices this week and is questionable to face off against Atlanta on Sunday. 
Dallas Cowboys LB DeMarvion Overshown (Hamstring) didn’t practice all week and is out for Sunday’s game versus the Commanders.
Green Bay Packers LB Lukas Van Ness (Concussion) is working his way through the league’s concussion protocol, and he’s questionable to play the Jets in Week 2. 
Houston Texans LB Jake Hummel (Groin) is out for Week 2 against the Bengals after not practicing during the week. 
Miami Dolphins LB Ronnie Harrison (Hamstring) missed practice all week and is out for Sunday’s game against San Francisco.
New England Patriots LB Dre’Mont Jones (Foot) is questionable to battle Pittsburgh on Sunday. 
New Orleans Saints LB Chase Young (Calf) is questionable, and LB Isaiah Stalbird (Shoulder) is doubtful to face the Ravens. Stalbird didn’t practice all week. 
Philadelphia Eagles LB Jonathan Greenard (Chest) is out for Week 2 against the Titans after being limited in practice all week.
Tennessee Titans LB James Williams (Elbow) and LB Cedric Gray (Concussion) are questionable to face the Eagles on Sunday. 
Washington Commanders LB Frankie Luvu (Groin) is out for Week 2 against the Cowboys after missing practice all week.
Defensive Backs
Arizona Cardinals CB Garrett Williams (Achilles) is out for Week 2, and CB Max Melton (Ankle) and S Dadrion Taylor-Demerson (Ribs) are questionable to face the Seahawks on Sunday. 
Atlanta Falcons S Billy Bowman Jr. (Foot) is out for Sunday’s game against Carolina, and CB A.J. Terrell (Shoulder) is questionable for the contest.
Baltimore Ravens CB T.J. Tampa (Knee) missed practice all week and will be inactive against the Saints. 
Cleveland Browns CB Tyson Campbell (Ankle) is questionable to face Tampa Bay on Sunday. 
Dallas Cowboys S Malik Hooker (Arm) missed practice all week and is out for Week 2 against Washington.
Kansas City Chiefs S Chamarri Conner (Knee) is out for Week 2, and CB Mansoor Delane (Shoulder) is questionable to face the Colts on Sunday. Delane practiced just on a limited basis on Friday. 
Las Vegas Raiders CB Darien Porter (Foot) missed practice all week and is out for Week 2 against the Chargers.
Los Angeles Chargers S Elijah Molden (Hamstring) is out for Week 2, and CB Deane Leonard (Abs) has been limited in practice all week and is questionable to face the Raiders. 
New England Patriots CB Carlton Davis (Neck) missed practice all week and is questionable to face the Steelers. 
New York Giants CB Paulson Adebo (Knee) was put on IR on Friday. After being limited on Thursday in practice, CB Deonte Banks missed Friday’s practice. 
New York Jets S Minkah Fitzpatrick (Groin) is out for Week 2 against the Packers. 
Philadelphia Eagles S Andrew Mukuba (Knee) is out for Week 2 against the Titans. 
Pittsburgh Steelers CB Joey Porter Jr. (Back) is out once again for Week 2 against New England. 
Seattle Seahawks S Ty Okada (Hamstring) is out for Week 2, and S Nick Emmanwori (Ankle) has been limited all week in practice and is questionable to face Arizona. 
Tampa Bay Buccaneers CB Jacob Parrish (Back) and S Miles Killebrew (Concussion) are questionable to face the Browns on Sunday. Killebrew fully practiced on Friday, and that should give him a chance to get activated Sunday.
Tennessee Titans CB Cor’Dale Flott (Leg) didn’t practice Friday and is questionable to face the Eagles on Sunday."""

            # Article 3: QB Breakdown
            article_3 = r"""MAFIA!! We are finally back! Another NFL season is here, and we’re ready to roll with the best team and site on the planet.
Each week, I’ll be breaking down my favorite quarterbacks on both DraftKings and FanDuel. Like always, the goal is to find the best point-per-dollar plays on the slate, but also to find quarterbacks with the upside to separate us in tournaments.
At quarterback, matchup is obviously important, but I’m also looking heavily at Vegas totals and how I think the game plays out. I want quarterbacks in games that have a chance to shoot out and, more importantly, games where they’ll have to keep throwing the football for four quarters.
That’s one reason I’m usually a little hesitant with quarterbacks who are massive favorites in GPPs. It doesn’t mean I won’t play them, but there’s always that risk they come out, score a few touchdowns, get up 20+ points, and we’re watching them hand the ball off the entire second half. I’d much rather attack a competitive game where both offenses are scoring, and our quarterback has to keep throwing.
Let’s get into it and take a look at my favorite quarterbacks for Week 2!
NOTE: For the first few weeks, I’ll still be using 2025 pass defense numbers when talking about matchups. Once we get to around Week 4 and actually have enough 2026 data to mean something, we’ll start using this year’s numbers.


QB Recommendations for Week 2
Carson Wentz, MIN $4,600 DK, $7,000 FD
Wentz should be in line to start this week with Kyler Murray in concussion protocol. We saw what he was able to do coming off the bench last week, completing 12 of 19 passes with three touchdowns. The biggest thing for me here is the price tag, especially on DraftKings, where I think he’s just too cheap for the offense and weapons he has around him.
Chicago’s defense gave up a 60% completion rate, 361 passing yards and 8.8 yards per attempt in Week 1, and that was against a Carolina offense that doesn’t come close to the weapons Minnesota has. Wentz doesn’t have to do anything crazy at this price tag to pay it off, and getting Justin Jefferson and the rest of these weapons at this salary gives him plenty of upside. If Murray is ruled out, Wentz will be one of my favorite value quarterbacks on the slate.
Dak Prescott, DAL $6,400 DK, $8,000 FD
Prescott played well despite losing to the Giants in Week 1, completing 22 of 30 passes for 175 yards and two touchdowns. He’s also played really well against this Washington team over the last two seasons, averaging 24.4 fantasy points per game against them.
Washington is coming off a Week 1 loss where they gave up three passing touchdowns to Jalen Hurts, and the biggest weakness in this secondary looks to be over the middle of the field and against the tight end. That sets up really well for Prescott, especially with Jake Ferguson and George Pickens both working those areas of the field. We know the upside Prescott has when this passing game gets going, and at his price tag I think there’s plenty of value here.
Lamar Jackson, BAL $7,300 DK, $8,800 FD
Jackson is probably your cash-game quarterback this week after putting up 324 total yards and two touchdowns in Week 1, with one of those coming on the ground. I do think there’s a little bit of a downgrade in the passing game with Zay Flowers dealing with an injury, but we’re not really playing Lamar because we need him to throw for 300 yards. We’re playing him because of everything he can do with his legs.
New Orleans just gave up 206 passing yards to Jared Goff, but the bigger thing for me is they also allowed 165 yards on the ground. That sets up really well for Baltimore to lean on Jackson and Derrick Henry in the run game. Lamar always has the upside to be the highest-scoring quarterback on the slate, and I think the combination of Jackson and Henry could give this New Orleans defense a lot of problems.
Caleb Williams, CHI $6,800 DK, $8,400 FD
Really impressive Week 1 for Caleb Williams, finishing with four total touchdowns, including two on the ground. What’s even more impressive to me is that I still think this offense has more upside. Williams didn’t even get Colston Loveland involved in the passing game, while Luther Burden and Rome Odunze combined for only seven catches and just over 100 yards. That’s pretty scary when you think about what this Bears’ offense could look like once all of these weapons start getting involved.
Minnesota’s defense also got torched through the air for the first three quarters last week, giving up 387 passing yards for the game. We saw the rushing upside from Williams in Week 1, and if we start getting more production from these receivers and Loveland, there’s a lot to like here. I think Williams has another big ceiling this week.
Trevor Lawrence, JAX $5,800 DK, $7,800 FD
Great Week 1 for Lawrence, missing only three passes on 21 attempts while throwing four touchdowns. One thing I’ve mentioned every single time I talk about Lawrence is that it’s going to be difficult to figure out which pass catcher will have the big game on a week-to-week basis. That being said, it was pretty clear in Week 1 that his top target was Parker Washington, who saw six targets for 83 yards and a touchdown.
The Broncos defense missed 28 tackles Monday night, and with all of the weapons Lawrence has on the outside, that could be a problem again this week. We might not know exactly which receiver will get there, but Lawrence doesn’t necessarily need us to. After what we saw from him in Week 1, I think there’s plenty of upside for another big game here.
Tyler Shough, NO $5,300 DK, $7,000 FD
I’m going right back to Shough this week just based on sheer volume. We know Baltimore will be able to score in this game, which means Shough should have to throw the football. It was a rough first half for him last week, where he had just one fantasy point going into the third quarter, but he ended up finishing with 29 DraftKings points after a monster second half, throwing three touchdown passes.
I think we will continue to see that type of passing volume this week, and we already know the connection he has with Chris Olave. If Olave can stay out of the medical tent, I really like that pairing again this week. The game script should force New Orleans to keep throwing, and at Shough’s price tag, I think there’s another path to a big game here.
Favorite Cash QB – Lamar Jackson
Favorite GPP QB – Carson Wentz"""

            # Article 4: RB, WR, TE Breakdowns
            article_4 = r"""Welcome to your weekly RB Breakdown, which is available every Wednesday during the season. This is an early look at the best RBs available on the main Sunday slate. It is essential to note that, since this article is posted mid-week, injuries and other news may alter the outlook as we approach Sunday.

Week 2 RB Breakdown
High Priced
Bijan Robinson – Falcons vs. Panthers (DK 8200 FD 8900)
The run blocking isn’t great right now, but the Falcons have no choice but to ride their stud. Cooper Rush appears to be starting again this week, which means plenty of dump-off passes to Robinson. He had 173 total yards and 29 touches last week, so expect more of the same. The Panthers were torched on the ground last week for 269 yards, allowing 7.5 yards per carry. They are dead last in run defense per PFF and run defense DVOA. Robinson is a cash and GPP option this week. He has 274 rushing yards and 4 TDs in his last two home games vs. Carolina.
Derrick Henry – Ravens vs. Saints (DK 7200 FD 8700)
The new-look Ravens offense got off to a great start, with Henry getting 144 rushing yards and 3 TDs. The Saints allowed 165 rushing yards to the Lions last week. The Ravens are 1st in run blocking per PFF, 2nd in run offense DVOA, and 7th in adjusted line yards. New Orleans is 22nd in run defense per PFF and 28th in run defense DVOA.  The only concern is that he doesn’t get four quarters if the Saints don’t keep the game competitive. Henry is a Cash and GPP option. 
Christian McCaffrey – 49ers vs. Dolphins (DK 8000 FD 9000)
The lack of rushing attempts in Australia is said to be caused by cramps, so a heavier workload could be on the table. The issue is that he probably shouldn’t get all the carries, as he’s not a good RB anymore but still a great receiver. The 49ers were 6th in run-offense DVOA and 1st in adjusted in-line yards, so their run blocking is still good. The Dolphins are 14th in run defense per PFF and 24th in run defense DVOA. Miami allowed Las Vegas 130 rushing yards last week. It will be interesting to see if he gets more carries in a game they should control. McCaffrey should find the end zone, so he is a cash and GPP option, but I think there are more explosive options in GPPs.
Mid-Priced
Bucky Irving – Buccaneers vs. Browns (DK 6100 FD 7900)
We expected more from Kenneth Gainwell, but Irving had 93 total yards and seven catches in a game the Bucs trailed throughout. The carries should increase with a better game flow this week, but we can’t expect the same number of catches. We did see more of Irving than Kenny Gainwell in the passing game. Tampa was 11th in run blocking per PFF and 4th in adjusted line yards in their limited rushing attempts. The Browns were 21st in run defense per PFF and 30th in run defense DVOA. Cleveland gave up 126 rushing yards to Jacksonville last week. Irving is a little priced up on FD. He is a solid GPP option. 
Breece Hall – Jets vs. Packers (DK 6200 FD 7200)
He racked up 102 rushing yards last week in a game they controlled throughout. New York was 7th in run blocking per PFF, 7th in run offense DVOA and 6th in adjusted line yards. The Packers allowed 107 rushing yards to a miserable Vikings run game. The Packers were 7th in run defense per PFF and 16th in run defense DVOA, so not terrible. This is a tougher matchup than last week for the Jets, but the Packers somehow blew that game last week. Hall is best left in GPPs, and I’m not sold on this Jets offense.  
Saquon Barkley – Eagles vs. Titans (DK 7000 FD 8300)
I was expecting a little more from Barkley last week, but he still had 83 rushing yards at 5.5 yards per carry. The Eagles’ defense couldn’t get off the field, which shouldn’t be an issue vs. the Titans this week, whose offense is horrific. The Eagles are 11th in run blocking per PFF, 20th in run offense DVOA, and 26th in adjusted line yards, so we need to see some better blocking. The Titans were 25th in run defense per PFF and 28th in run defense DVOA. This is a great matchup for Barkley, so he is a Cash and GPP option. 
D’Andre Swift – Bears vs. Vikings (DK 6300 FD 7100)
Swift had a monster game last week, with 124 rushing yards and 3 rushing TDs. He got most of the work while the game was still close. The Bears were 6th in run blocking per PFF, 1st in run offense DVOA and 2nd in adjusted line yards. The Bears ran for 291 yards last week. The Vikings were 4th in run defense per PFF and 4th in run defense DVOA. They faced a weak offensive line and below-average running backs. This Bears offense has taken the next step, and while not an easy matchup, Swift is still a Cash and GPP option. 
Ashton Jeanty – Raiders vs. Chargers (DK 6800 FD 7700)
The new offense looked good on Jeanty, who had 147 total yards and 2 TDs last week. He looked a little tired in the 4th quarter, with no training camp to heal his ankle injury, so he basically did all of that in three quarters. The Raiders ranked 12th in run blocking per PFF, 12th in run offense DVOA, and 10th in adjusted line yards. The Chargers offense was awful last week, and their run defense was not great. They were 13th in run defense per PFF and 23rd in run defense DVOA. The Cardinals ran for 116 yards against LA last week. Jeanty may not match last week’s production but should still get solid numbers as long as Kirk Cousins is serviceable. He is a Cash and GPP option.
Javonte Williams – Cowboys vs. Commanders (DK 6400 FD 7400)
He has 72 total yards and 2 TDs even though the Cowboys did not have the ball much. Williams is the only RB they have at this point with Malik Davis injured, so he’ll get all the action he can handle. The Cowboys were 14th in run blocking per PFF, 18th in run offense DVOA, and 11th in adjusted line yards. The Commanders were 29th in run defense per PFF and 13th in run defense DVOA.  They allowed Barkley to run for 5.5 yards per carry. Williams is a solid cash and GPP option. 
Low Priced
Chuba Hubbard – Panthers vs. Falcons (DK 5800 FD 6300) 
All the talk was about Jonathan Brooks in the preseason when Hubbard got hurt, but Week 1 didn’t live up to the hype for Mr. Brooks. Hubbard had 13 touches compared to Brooks’ five. Chuba also scored twice. Carolina is 4th in run blocking per PFF, 15th in run offense DVOA, and 3rd in adjusted line yards. The Falcons are 17th in run defense per PFF and 7th in run defense DVOA, but that was against the Steelers, who did not try to run the ball. Hubbard still has some risk but is an option in GPPs at his low price on FD.

Week 1 is officially in the books! Big congrats to last week’s winners and let’s keep the momentum going into Week 2. For those new here this season, I hold myself accountable in this weekly column with a quick review focusing on the misses from the previous week. The Wide Receiver position is highly volatile, but the primary focus is finding the right blend of high target volume and plus matchups at various price points.
Week 1 Misses:
Ja’Marr Chase (2-12-0, 4 targets)
Jameson Williams (4-45-0, 9 targets)
Chris Godwin (4-40-0, 4 targets; 1-3-0 rushing)
Marvin Harrison Jr. (1-33-0, 3 targets)
Chase had one of the more bizarre receiver performances in Week 1. He posted the second-fewest yards in a game in his career in a game where his team scored 33 points. Sometimes weird things happen in a sport with an oblong-shaped ball.
Jamo drew nine targets, hauling in four for 45 yards. He sported a 23% target share and a 54% Air Yards share in a game that cleared 60 total points. He had the single highest delta between expected fantasy points (19.7) versus realized fantasy points (8.5) among all WRs last week. This is a process over results column. I’d recommend Jamo in the exact same matchup any time.
Godwin is the first bleak recommendation where I’ll take heat. He looked cooked. Not helping his case in this matchup, we saw Baker Mayfield throw a career-high 43% of his pass attempts behind the line of scrimmage. Short underneath targets raise the floor, but this was a ceiling capped outing due to his quarterback and possibly (?) his new OC. I’ll be closely tracking Week 2’s outing against a Browns defense that Trevor Lawrence carved up with ease.
The final L here is Marvin Harrison Jr. Considering ~30% of Survivor pool players took the Chargers, I’m not the only one floored by the gamescript here. What was most damning for Marv’s future was the receiving role he was put in under this new offensive scheme. 19.9% of his routes were “go routes” last year. That rate spiked all the way up to 34.4% in Week 1. It wasn’t just a shock to the structure of Arizona’s passing attack. That rate led all wide receivers across Week 1 and is a scary harbinger for volatility in weeks to come.
On to Week 2!
It’s important to note this article is posted mid-week, so injuries and other news can change our reads as we get closer to Sunday. This article is specifically for Sunday’s “Main” slates, so WRs from Thursday, Sunday, and Monday Night Football are not considered.

Player Pool
CeeDee Lamb (DAL) vs WAS [$7,300 DK, $8,500 FD]
Dallas didn’t look phenomenal in the opener, but they also got bullied by a run-heavy Giants attack that sapped away playing clock. In the second half alone, the Giants posted drives of 12, 13, and 12 plays that went for 8:01, 8:11, and 5:21, respectively. It did not leave much opportunity for the Dallas offense, one that started slowly with back-to-back drives ending in punts. Despite that hurdle, Lamb accrued eight targets for a 5-44-1 stat line. He should find even more success this week against a Commanders secondary that leaned heavily into zone coverage and two-high. Lamb paced the team in YPRR against both schemes last year (2.38 vs zone, 2.15 vs single-high). The Commanders gave up a 70% catch rate and the third most fantasy points to the slot in Week 1. Lamb sports inside/outside versatility and the Commanders’ starting trio of corners present minimal matchup difficulty.
Chris Olave (NO) @ BAL [$7,200 DK, $7,900 FD]
Olave was in and out of the lineup frequently visiting the medical tent in Week 1, but between his breaks, he found a way to turn 13 targets into a 10-182-0 stat line. Olave paced all receivers last week in receiving yards as he posted a career-high mark. He’ll look to keep that success going in a matchup where the Saints are 8.5-point road underdogs. Jesse Minter’s Ravens played a ton of two-high in the opener (third highest rate). Dating back to the start of the 2025 season, Olave sports a 24% TPRR mark, 1.98 YPRR, and 0.46 FP/RR against two-high coverage shells. With Olave coming off a 29.3% first-read performance, I see nothing wrong with finding the salary for a player coming off heavy usage in what projects to be trailing gamescript.
Zay Flowers (BAL) vs NO [$6,700 DK, $7,600 FD]
We saw the Lamar Jackson-Flowers connection pick up right where they left off last year with Flowers exploding for 6-150-1. Flowers left midway through the second quarter due to a hamstring injury, so we’ll need to monitor his practice reports throughout the week. It did not seem serious, but a full participation mark on Friday would lean toward Flowers entering my player pool. Flowers was a target last week due to his matchup against the Colts’ single-high coverage scheme. New Orleans deployed single-high at the third highest rate last year (59.8%) and carried that over to Week 1 (58.5%). Flowers was the WR7 in target share (29.5%), WR10 in first-read rate (33.8%), and WR9 in YPRR (2.85) against single-high coverage last year. A Lamar/Zay skinny stack with an Olave bring-back feels like a smart way to begin DFS lineups this week.
Mike Evans (SF) vs MIA [$6,600 DK, $8,200 FD]
The 49ers sport the highest spread in their favor on the main slate (-13.5) and many will shy away from the passing attack in fear of blowout potential. There’s a very good chance that the 49ers reach their implied team total *because* Brock Purdy and this passing attack hits their ceiling. Evans looked sharp in the opener, turning seven targets into a 6-49-1 receiving stat line. He’ll square off against a rag-tag group of corners for Miami that features JuJu Brents and Jason Marshall Jr. on the outside. Brents sports a 38.9 PFF Grade after one week and Marshall sported a 40.8 PFF Grade last year as a part-time player. Miami played single-high at the league’s third highest rate last week (71.0%) which will create plenty of 1-on-1 opportunities for Evans against this duo on the outside. Advantage, Evans. Evans is priced as the WR5 on FD, but down at WR9 on DK this week.
Parker Washington (JAX) @ DEN [$5,900 DK, $6,600 FD]
Washington hit the ground running in the season opener, turning six targets into a 5-83-1 stat line. The Jaguars buried the Browns in that matchup with Washington resting for much of the fourth quarter. This week he draws an interesting matchup between two AFC contenders taking on a downtrodden Denver defense. The Broncos’ offensive playcaller changes were notable on MNF, but DC Vance Joseph has long held his position. The defense was embarrassed, missing tackles left and right. Washington is an elusive playmaker with the ball in his hands and should help contribute to this missed tackle tally. He also draws a schematic advantage with Denver skewing man-heavy. Dating back to the start of last season, Washington sports a 2.93 YPRR and 25% TPRR mark against man defense. We also saw Washington post a big outing on this defense in Week 16 last year. On a 55.7% snap share, Washington turned 10 targets into a 6-145-1 stat line with four missed tackles forced and 80+ yards of YAC.
Luther Burden (CHI) vs MIN [$5,700 DK, $6,000 FD]
Bears/Vikings presents an interesting divisional matchup that could see plenty of points. I expect us to target this Bears defense in this column consistently in 2026, but this is a good spot for the Bears offense to also put up points. Caleb Williams was QB3 in EPA/dropback against the blitz last season sporting a meager 3.3% sack rate (dead last among qualifying QBs). No team blitzed more than Flores last season and he opened the year with a ridiculous 71.7% blitz rate in the opener against Green Bay. Against the blitz last year, Burden sported an elite 3.81 YPRR (WR4) and 0.65 FP/RR (WR6). His 40.0% first-read rate is what really stands out as the blitz does not allow much time for progression reads. The Bears run game was firing on all cylinders against the Panthers’ porous run defense in Week 1. In Week 2, it’s the passing attack’s turn. Burden’s pricing on FD is astoundingly low.
Romeo Doubs (NE) vs PIT [$5,000 DK, $5,800 FD]
Fortune favors the bold in DFS. You have to be bold to go to Romeo Doubs after his Week 1 showing. Doubs failed to bring in any of his three targets in the opener (including a wide-open drop). Following news of A.J. Brown’s injury, Doubs elevates to top of the receiver depth chart. Doubs signed a 4-year, $68M contract this offseason. He’ll take on a Steelers secondary that has some injuries on the backend (and contract holdouts), making this a unit we can target. Against an inept Atlanta offense last week, DC Patrick Graham turned to a zone-heavy approach (100% of snaps!) that strictly played Cover-3, Cover-4, and Cover-6. In his final year with Green Bay, Doubs sported a 21% TPRR, 14.1 aDOT, and 2.07 YPRR against these coverages combined. Drake Maye threw for 268/2 (75.7% completion rate) against this defense last year in Week 3. Tournament-only recommendation.
Matthew Golden (GB) @ NYJ [$4,700 DK, $5,900 FD]
Golden had a slow rookie year, but the Week 1 usage was extremely promising. Golden sported a team-leading 82.1% snap share, team-leading 40 routes, and team-leading 11 targets. The Packers draw a Jets defense that has two very suspect corners on the perimeter. RCB Brandon Stephens gave up the 10th highest passer rating when targeted last year (126.4) thanks to him allowing eight touchdowns in his direct coverage per PFF (No. 2 among all CBs). LCB Azareye’h Thomas gave up a team-high 14.8 YPR in coverage (No. 12 among all CBs). Last week we saw Christian Watson connecting with the deep bomb for a touchdown, but it was Golden that was more consistently utilized. Both are in play this week (as are Jordan Love doubles), but Golden’s pricing stands out as a nice value play on both sites.
Other WRs of Note: Jaxon Smith-Njigba, Jordan Addison
Week 2 Wide Receiver Punts
Devaughn Vele (NO) @ BAL [$4,200 DK, $5,500 FD] – Vele came through for us last week as our Sub-5% GPP Play with flying colors. After a slow start, Vele ended the day with a 7-69-1 stat line off nine targets. This is going to be a pass-heavy, fast-paced offense and Vele is a full-time receiver opposite Olave. This bargain pricing won’t last forever.
Caleb Douglas (MIA) @ SF [$3,700 DK, $5,100 FD] – Douglas was in my initial writeup for this column last week, but the late steam for Chris Bell playing with “zero restrictions” led to him being omitted from final publication. We talked about him on the DFS Livestream as a min-priced punt ($3K) that opens the door for jamming in Jahmyr Gibbs and other studs and he delivered – 5-94-0 on seven targets. Malik Willis is a boom/bust thrower deep down the field and Douglas is his top downfield target right now. Better punt on FD.
Jaylin Noel (HOU) vs CIN [$3,700 DK, $5,200 FD] – Nico Collins suffered a midweek injury in practice tweaking his hamstring. His status is unclear at this time, but it’s a pretty intriguing matchup for Noel in the slot. Last year the Bengals were a legitimate slot funnel, giving up the fifth fewest FPPG to perimeter receivers and the fifth most to the slot. Noel sported a 74.3% slot rate last year (83.3% in Week 1) where he’ll take advantage of the plus matchup versus slot CB, Jalen Davis. Better punt on DK.
Sub-5% Ownership GPP Play
*Will update this section Sunday morning after getting a better feel for ownership and roster construction.*

The tight end position has become a vital part of a football team’s success, and it is also an important part of our fantasy success. Tight ends can sometimes make or break your fantasy week as this position can help you get to the top of the leaderboard or sink you down to the bottom. When digging in and selecting our tight end options for the week, we’ll consider snap count, targets, opportunities, and weekly matchups while also taking into consideration any depth chart movement or medical news. 
Although it’s challenging to check all the boxes, we aim to identify players with the most upside while also providing with a safe floor. Each site assigns a salary to players, and in close comparisons, we may use salary points to decide on the TE to use. The focus of this article will be on the tight end slot in the roster construction and not on the flex spot. Some strategies include using double tight ends in the same lineup, especially in MME GPPs, while correlating with their quarterbacks in GPPs to maximize the position.
Please note: This article will focus on my top selections of the week, including deep fliers or punts for tournaments. I will make sure to try and specify if there is someone that I feel is strictly a cash game play or a tournament only play. 
Now, let’s examine the options for Week 2 on the two major sites (DraftKings and FanDuel) for their main primary Sunday contest. I will also be in the NFL Discord throughout the weekend to discuss the TE options, so make sure to ask me any questions there!
2026-2027 Top Tight Ends (PPR ranking)


Defenses vs. TE- 2026

Week 1 Recap

While we had a few zeros during the first Week, I would consider it a pretty large success overall. We had the top two scoring tight ends on the main slate in McBride and Goedert, and guys like Johnson, Hockenson, and Mayer all hit value. It was very disappointing to see Loveland only get two targets, especially during a game in which the Bears put up 50 points but we have to give Carolina credit as they took him out of the game and made Caleb look elsewhere. Time to regroup and move on to Week 2!
Week 2 Analysis 
Preferred Plays 
Trey McBride, Arizona Cardinals ($6,900 DK/$7,500 FD): Trey McBride silenced any doubters in Week 1 as he led all tight ends on the main slate with nine catches on 12 targets for 95 receiving yards and a touchdown. McBride is certainly the focal point in this Cardinals passing attack and even with a new offensive system in place in Arizona, the connection between Brissett and McBride is as strong as ever. While the matchup appears to be tough against Seattle, McBride actually did well against the Seahawks in 2025 as he had 16 catches on 24 targets for 179 receiving yards and a touchdown. He is the most expensive tight end option on the slate, but I think we can get lower ownership on him and I will be eyeing him up for tournament lineups. (GPP)   
Dallas Goedert, Philadelphia Eagles ($4,800 DK/$5,700 FD): The price point jumped rather quickly for Dallas Goedert, so we might get another week or so before he goes above the 5k plateau over on DraftKings. Goedert had a strong Week 1 as he brought in five of seven targets for 77 yards while finding the end zone twice, and clearly, his red zone presence will continue to be felt, especially with the lack of receiving weapons in Philly. The Eagles are heavy favorites against the Titans this week and if they get out to a strong lead, the opportunities for Goedert might be limited, so I will just be viewing him as a tournament option this week. (GPP) 
Mark Andrews, Baltimore Ravens ($4,400 DK/$5,200 FD): It was great to see the Lamar Jackson and Mark Andrews connection come alive in the first week of the season and I think it could last all season long. Andrews brought in four of six targets for 49 yards and it certainly helps that he doesn’t have Isaiah Likely looking over his shoulder any longer. In addition, he could see an even more elevated role in the coming weeks as Zay Flowers is dealing with a hamstring and Ja’Kobi Lane is tending to a fractured wrist, so between the potential opportunities and his strong rapport, I think Andrews could be looked at in both cash and tournament settings. (Cash + GPP)
Harold Fannin Jr., Cleveland Browns ($4,100 DK/$5,500 FD): It was a quiet Week 1 for Harold Fannin Jr., but I believe this week he could make much more of an impact and could be a fantasy asset. He was held to two catches on three targets for 21 yards against Jacksonville, but they now get to face a softer Buccaneers defense that got gashed by Mike Gesicki, who hauled in five catches on seven targets for 78 yards and a touchdown. Of course, part of Fannin’s overall success will depend on the play of his quarterback, so that is where the risk comes in, but given the overall matchup and his ability to win in the end zone, I think he could be a lower-owned tournament target for us this week. (GPP)
Punt/Value Options 
Hunter Henry, New England Patriots ($4,000 DK/$5,000 FD): The value tight end that carries the most upside this week could be Hunter Henry. He was kept in check in Week 1 but could be a candidate for a strong rebound performance here in Week 2. AJ Brown will be out for the Patriots for at least four games, so Henry’s role could be elevated for the foreseeable future. The matchup against the Steelers looks very tough as they kept Kyle Pitts in check but I think that was more due to the quarterback play than anything else. Hunter Henry had a strong outing last year against the Steelers as he brought in eight of 11 targets for 90 yards and two touchdowns, and while we shouldn’t expect the two touchdown performance, I think 40-50 yards and one end zone visit could certainly be in play. (GPP)
Jake Ferguson, Dallas Cowboys ($3,800 DK/$5,400 FD): I think my favorite value tight end this week is Jake Ferguson. Sure, he only had two targets for six total receiving yards, and that alone will scare people away, but that Giants defense is vastly improved and he now gets a way better matchup against Washington this week. Ferguson found the end zone three times last year against the Commanders and we just saw Washington struggle against Dallas Goedert as he found the end zone twice. Washington will have their hands full with containing Lamb and Pickens, which will only leave Ferguson in better matchups over the middle of the field, and I think he will find his way into the end zone this upcoming week. (Cash + GPP)
Michael Mayer, Las Vegas Raiders ($3,600 DK/$5,300 FD): Mayer was perfectly fine as a punt/value option and as long as Bowers remains out, he needs to be up for consideration. There is a chance that Bowers can be back in the lineup this week, so we do need to follow that news, but if not, Mayer should be considered once again for cash and tournament builds. He brought in six of seven targets for 32 yards and we were spot on about Kirk Cousins looking his way often. Mayer was used closer to the line of scrimmage, so he might not be the type to go for 50+ yards, but he can certainly rack up catches and probably offers better upside on a full PPR site like DK. (Cash + GPP)
TJ Hockenson, Minnesota Vikings ($3,500 DK/$5,100 FD): We had our eye on Hockenson last week and I am definitely not opposed to looking his way again. Hockenson was second on the team with five targets in Week 1 and he was able to connect with backup quarterback Carson Wentz in the end zone, so there is some excitement about what he might be able to bring us throughout this season. Chicago’s defense does not look great and it could have been even worse if a Darren Waller touchdown was not negated in the first quarter by a flag. I think Hockenson gets us cheap exposure to what could be an exciting NFC North matchup, and I think he could be an option for us in all formats while his price is still this low. (Cash + GPP)"""
            
            # Load exact text to the DB
            payload = [
                ("Week 2 Cash Game Breakdown & Matchups", article_1),
                ("Week 2 Injury Report", article_2),
                ("Week 2 QB Breakdown", article_3),
                ("Week 2 RB, WR & TE Breakdowns", article_4)
            ]
            
            cur.executemany("INSERT INTO raw_slate_articles (title, content) VALUES (?, ?)", payload)
            conn.commit()
            
            print("   ✅ All 4 articles successfully uploaded directly into action_grid.db.")
            print("   ✅ Data is stored raw, unedited, and completely unmanipulated.")
            
    except Exception as e:
        print(f"   ❌ Execution Failed: {e}")

    print("=" * 65)

if __name__ == "__main__":
    upload_raw_articles()
