
[![Build Status](https://travis-ci.com/DataScienceDiscord/Charlotte.svg?branch=master)](https://travis-ci.com/DataScienceDiscord/Charlotte)
[![Coverage Status](https://coveralls.io/repos/github/DataScienceDiscord/Charlotte/badge.svg?branch=master)](https://coveralls.io/github/DataScienceDiscord/Charlotte?branch=master)
[![Build Status](https://img.shields.io/discord/464539978442211328.svg?logo=discord&logoWidth=18&colorB=7289DA)](https://discord.gg/UYNaemm)


**Charlotte** is a small discord bot with its own lightweight interface to the discord gateway and rest api. The bot is intended to be used as a learning tool for the users of our discord channel. The small code base makes it easy to dive into the project and the continuous integration will enable the contributors to discover and understand a basic development workflow, from discussing features, to implementation, testing, documentation and deployment as well as some basic aspects of version control and working in a team.  
We hope to be able to add data science related commands that will allow the contributors to practice their data preprocessing, SQL and plotting skills (and possibly ML in the future).

## Applying

If you want to follow the course, you should read the following documents:
https://github.com/DataScienceDiscord/Charlotte/blob/master/applying.md

## Commands

Commands can be called using the following format: **!c/command/parameter**

**top**  
*Returns the #n most active users (by number of messages).*  
Parameter: Number of users to return. (<=9)  
Example: `!c/top/9`  
Output:  
![top output](https://raw.githubusercontent.com/DataScienceDiscord/Charlotte/master/static/top.png)  

**say**  
*Repeats the given sentence.*  
Parameter: Sentence to say.  
Example: `!c/say/hello`  
Output:  
![say output](https://raw.githubusercontent.com/DataScienceDiscord/Charlotte/master/static/say.png)  

## Contributing

Read the docs: https://datasciencediscord.github.io/Charlotte-Documentation/index.html

### Installing

Ensure you have Python 3 and git installed and execute the following commands:
```
git clone https://github.com/DataScienceDiscord/Charlotte.git
cd Charlotte
pip install -r requirements.txt
```

You'll have to setup your postgres installation so that it matches the `database/config.py` file or vice-versa.  
Once you have created and configured your two databases (`charlotte` for dev and `charlotte_test` for test) you'll need to initiate the appropriate tables using the following command and the appropriate `ENVCHARLOTTE` environment variable:

`python -m scripts.init_tables`

### Running the tests

The `ENVCHARLOTTE` environment variable should be set to `TEST`.  
From inside the Charlotte directory:  

`pytest --cov=. tests/ --cov-config .coveragerc`

All tests should pass before a commit and the coverage percentage should not go down from previous commits.

