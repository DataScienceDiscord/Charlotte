# Charlotte Application Process

**Unless otherwise specified, no parts of this document are optional or superflous, please do not skip any!**

This course is meant to be applicative, that is to say it's based on the principle that you'll learn most from doing rather than reading. The only way to learn is to struggle and this course will not hold your hand or give you premade solutions, you're supposed to do your own research and ask when you get stuck. At each step a prerequisite section gives you a short introductory reading list to the concepts that will be used in that step. You can complement it by your own research and using google.  
A basic understanding of python is required, you should be familiar with the basic data structures and control statements (conditions, loops, etc...). If you aren't I'd advise you follow any online python course, which should introduce you to the basic concepts in a dozen hours or so and enable you to follow this course.

Thoughout this course you'll learn the following soft and hard skills:
* Using version control and its workflows (commits, pull requests, merges, conflicts, ...).
* Collaborating on a project, discussing features, asking productive questions.
* Autonomous problem solving, tracking exceptions and errors, troubleshooting, searching google effectively, reading documentation.
* Databases, SQL, using an ORM (object relational mapping) layer.
* Writing effective unit tests and using a testing framework.
* Documenting your code, meaningfully using comments, writing clean code.
* Interacting with online APIs.
* Processing, cleaning and visualizing data (depending on what type of command you implement).


## Prereq:
Read this short introduction about asking questions:
```
When asking a question about code, make sure your question is specific and provides all information up-front. Here's a short checklist of what to include. For more details about each section, continue reading this page.

    A concise but descriptive title.
    A good description of the problem.
    A minimal, easily runnable, and well-formatted program that demonstrates your problem.
    The output you expected, and what you got instead. If you got an error, include the full error message.

Do your best to solve your problem before posting. The quality of the answers will be proportional to the amount of effort you put into your post.


Writing a good description of the problem

When describing your problem, include as much useful information as possible. Try and include as many of the below pieces as possible -- the more info you include, the higher the chances of getting a useful response:

    What is your code sample you provided supposed to do?
    What exactly is the problem you're seeing?
    What is the expected output or behavior of your program?
    What output or behavior do you get instead?
    If your code doesn't compile or crash, is there an error message of any kind? If so, what is it? If not, what happened?
    What have you already tried to debug your own problem? Where do you suspect the problem is? What uncertainties do you have?
    What precisely are you confused by?

The expectation is that you've spent some time trying to solve your question and polishing your question before you post it.

In the event that you do your own research and come up dry, be sure to mention what you've already tried/searched for as well as what the results were. This will guide people in helping you and also open up your research techniques to scrutiny and improvement.

Some other DOs and DON'Ts:

    DO try and be concise. It's important to include as much info as possible, but you also don't want to waste people's time by including irrelevant details.
    DO NOT link to some other website where you asked your question (e.g. Stackoverflow), because we do not want to discuss the same problem in different places. Your question should be complete and self-contained. When you post a question on one website, wait a day or two to give people time to answer your question. Don't simultaneously post -- that just means double work for people who take time to reply.
    DO NOT use this this channel as a proxy for Google. Please put in genuine and significant effort into solving a problem for yourself first before posting it in this channel. Otherwise, not only are you wasting everyone's time, you are doing yourself a disservice. Finding information and doing your own research is one of the most important skills a programmer can have. The only way to get better at it is by taking the initiative and looking for existing information yourself. Only then ask others for help.
```
*Source (reworded slightly): https://www.reddit.com/r/learnprogramming/wiki/index#wiki_getting_debugging_help*
All questions about this course should be asked on the **#colab** channel.


# Project Setup

Ideally you should do this part by yourself, searching google for answers when you encounter a problem. This is an autonomy threshold you should pass to be able to qualify for the rest of the course.
Each step should take no more than 15 minutes. If you get stuck you can ask on **#colab** but this should only come after having searched by yourself extensively on google.

## Git setup

**Prereq:**
* Look at this video introduction to version control and git: https://www.youtube.com/watch?v=uUuTYDg9XoI
* Or if you'd rather read text: https://stackoverflow.com/questions/1408450/why-should-i-use-version-control

**Steps:**
* Install **git**
* Create a github account
* Fork the Charlotte repository into your account
* Clone the forked repository to your computer using git clone

## Database Setup

**Steps:**
* Install **postgresql**
* Create a database named charlotte_test
* Define an environment variable called ENVCHARLOTTE and set it to TEST

## Project Setup

**Prereq:**
* Read this introduction to virtual environments and what they're used for: https://pythontips.com/2013/07/30/what-is-virtualenv/


**Steps:**
* Install python 3.6 or above.
* Create a virtual environment called "venv" using **virtualenv** in the Charlotte folder
* Activate it.
* Install the requirements in that virtual environment using **pip**
* Update the TEST part of the **database/config.py** file to reflect your postgres configuration (user, port, etc ...).
* Create a .database_secret (no extension!!) file in the root folder of Charlotte and write your postgres password in it.
* Run `python -m scripts.init_tables` to create the necessary tables in your test database
* Run tests and ensure no errors are raised using **pytest**

# Choosing your command


**Steps:**
* Open the Charlotte documentation and find the part about commands, this should explain clearly what a command is and what it should look like.
* Look at the system diagram in the documentation and read the documentation as needed and try understand what each system does.
* Choose a command to implement and fill the blanks in this template:
```
Single line description of my command:
_________________________________________.
My command is useful because (one line):
_____________________________________
My command will be called: ______
My command will take the following parameters:
___________________
For example, to call it my users will write in chat:
!c/______/_________"
My command (will/will not) return a message.
My command (will/will not) return a plot.
Read the documentation of the database module: https://datasciencediscord.github.io/Charlotte-Documentation/_generated/database.html
Each submodule (excluding base_model, config and database) corresponds to a table. The fields of the submodules correspond to columns of these tables.
My command (will/will not) interact with the database.
My command (will/will not) require a new attribute in an existing table.
My command (will/will not) require a new table.
```
* Open an issue titled "My Application (your_discord_name#your_discord_number)" in the main Charlotte repository (not the fork.)
* Paste your command template in the issue's body.
* Wait for an answer to your issue where we will discuss feasability, whether it fits into Charlotte's scope, and whether it's redudant as well as other potential problems.
* Once the discussion is concluded open a pull request (with an apt name) from your fork referencing this issue.

# Implementing your command

**Implementation should only ever come after discussion, otherwise your time will be wasted. Part of collaborating is agreeing upon specifications and requirements and no coding can be done before this step has been completed.**

**General prereqs:**
* Read this python style guide (**Important!** Writing good code is ensuring it's clean and understandable to the people who'll read it after you): https://docs.python-guide.org/writing/style/

If you have questions about these prerequisites, or are unsure about best practices, as always feel free to ask on **#colab**.

## Create the new command

**Prereq:**
* Read the charlotte documentation https://datasciencediscord.github.io/Charlotte-Documentation/index.html and understand how a message makes it from the chat and the discord server to the bot, and how the commands of the bot interpret and send back messages.
* Read about how to use git to commit your first piece of code (note that your github repository will already be connected to your local folder if you cloned it, so there will be no need to add a remote origin): https://readwrite.com/2013/10/02/github-for-beginners-part-2/

**Steps:**
* Write a list of inputs, a list of outputs, and a list of potential errors for your command.
* Post them as a reponse to your issue.
* Create a new file in the commands module for your command, following the naming conventions.
* Create a new function in your command file and make it raise a `NotImplementedError`.
* Add a docstring to this function to describe what it does, using the same convention as the other docstrings in the codebase. If you follow the correct format your docstring will be used to automatically generate HTML for the online documentation website once your pull request has been merged.
* Commit and push your changes to your pull request. 


## Writing the database interface

**If your command does not interact with the database you can skip this step.**

**Prereq:**
* Watch this video introduction to databases and SQL (1.5x speed recommended): https://www.youtube.com/watch?v=FR4QIeZaPeM
* Or read this text introduction: https://www.guru99.com/introduction-to-database-sql.html
* Read these short explanations of relational database concepts:
	* https://www.sqa.org.uk/e-learning/SQLIntro01CD/page_03.htm
	* https://www.sqa.org.uk/e-learning/SQLIntro01CD/page_07.htm
	* https://www.sqa.org.uk/e-learning/SQLIntro01CD/page_08.htm
	* https://www.sqa.org.uk/e-learning/SQLIntro01CD/page_09.htm
* Read this introduction to the peewee ORM layer: http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#model-definition
* Read the code of the `database.database` module.
* Read this short introduction to unit tests: https://stackoverflow.com/a/3258768
* Read this short introduction to the assert statement: https://www.programiz.com/python-programming/assert-statement

**Steps:**
* If your command requires a new table, create a new model  in the database module.
* If your command requires a new field in an existing table, update the models in the database module.
* If your command requires information that isn't accessible through existing methods in the database.database module, create a new method in the database.database module and the necessary query.
* Add the necessary tests to cover the code you added to the database module.
* Ensure all tests pass and push your changes.


## Implementing the function

**Prereq:**
* Read this article about python exceptions: https://swcarpentry.github.io/python-novice-inflammation/07-errors/index.html
* When you encounter an exception, check its meaning here: https://docs.python.org/3/library/exceptions.html
* If your function requires plotting, read this short introduction: https://matplotlib.org/users/pyplot_tutorial.html

**Steps:**
![Draw the owl image](https://a.thumbs.redditmedia.com/ffMlolOIyiBMc93PCTyeJLqhf9xfi_LFfl2pzycwtF4.png)
* Draw the rest of the fucking owl.

Joking aside, there is no way to give specific advice on this part. The implementation of your function depends on what it does. Try to write a small pseudocode implementation and ask for advice on **#colab** or in your issue.


## Writing the unit tests

**Prereq:**
* Read this short introduction to unit tests: https://stackoverflow.com/a/3258768
* Read this short introduction to the assert statement: https://www.programiz.com/python-programming/assert-statement


**Steps:**
* Create a new file in the `tests` folder following the file naming convention used by the other tests.
* Write an aptly named test for each input/output/error combination that can occur in your function.
* Run pytest and ensure all tests pass.

# Finalize the course

Once all this has been done your pull request will be merged and your code will be automatically deployed to Charlotte's server. Everyone will then be able to use your new command on the server.
