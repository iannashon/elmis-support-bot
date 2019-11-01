import logging
import requests
import telegram


from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, MAIN_MENU, ORDER_STATUS, ORDER_STATUS_PROGRAM,DISTRICT_REPORTING_RATE_PROGRAM, DISTRICT_REPORTING_RATE, COMING_SOON, SELF_CARE, DESCRIPTION, CONFIRM, VIEW_TICKET_BY_KEY, SEARCH_TICKET_BY_KEY, ACCESS_ACC_STEPS, ACCESS_ACC_STEPS_TWO, CLEAR_CACHE_STEPS, CLEAR_CACHE_STEPS_TWO , HELP, FILL_LOGIN_CREDENTIALS, SIGN_IN, CLEAR_CACHE, ADD_PRODUCT, ADD_PRODUCT_STEP_TWO, GET_PROGRAME_NAME, GET_MSD_CODE, MIN_REPORT, START, RNR_STATUS, SUBSCRIBE_MENU= range(30)

bot=telegram.Bot(token='711948397:AAF1NNp3m1uWkcCyttkGVVQd21UzQakIfRg')

# TESTING
# API_ENDPOINT = "http://localhost:9091/new-api/support/createNewIssue"
# API_GET_RNR_STATUS_ENDPOINT = "http://localhost:9091/rest-api/support-desk/getLatestRequisitionByFacilityCode"
# API_SUBSCRIBE = "http://localhost:9091/rest-api/support-desk/addSubscribers"

# UAT
# API_ENDPOINT = "https://uat.tz.elmis-dev.org/new-api/support/createNewIssue"
# API_GET_RNR_STATUS_ENDPOINT = "https://uat.tz.elmis-dev.org/rest-api/support-desk/getLatestRequisitionByFacilityCode"
# API_SUBSCRIBE = "https://uat.tz.elmis-dev.org/rest-api/support-desk/addSubscribers"


# PRODUCTION
API_ENDPOINT = "https://elmis.co.tz/new-api/support/createNewIssue"
API_GET_RNR_STATUS_ENDPOINT = "https://elmis.co.tz/rest-api/support-desk/getLatestRequisitionByFacilityCode"
API_SUBSCRIBE = "https://elmis.co.tz/rest-api/support-desk/addSubscribers"

next_keyboard = [[InlineKeyboardButton("Next", callback_data='Next')]]
main_menu_keyboard = [[InlineKeyboardButton("Main menu", callback_data='Main menu')]]
main_menu = [[InlineKeyboardButton("Mini Reports", callback_data='Mini Reports')], [InlineKeyboardButton("Help/FAQ", callback_data='Help/FAQ')]]
reply_keyboard = [['Mini Reports', 'Help/FAQ']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
main_menu_inline_keyboard = InlineKeyboardMarkup(main_menu)


def start(update, context):
    welcome_html_string = ('<b>Hello ' + update.message.chat.first_name.upper() + '!</b> \n'
                            'Welcome to eLMIS Support Desk \n\nWhat can I help you with?')
    update.message.reply_html(welcome_html_string, reply_markup=main_menu_inline_keyboard)
    return START


def main_menu(update, context):
    query = update.callback_query
    welcome_html_string = ('<b>Hello ' + query.message.chat.first_name.upper() + '!</b> \nWelcome to eLMIS Support Desk \n\nWhat can I help you with?')
    query.message.reply_html(welcome_html_string, reply_markup=main_menu_inline_keyboard)
    return START

def start_menu(update, context):
    query = update.callback_query
    if query.data == 'Mini Reports':
        return mini_reports(update, context)
    else:
        return help(update, context)



# Help/FAQ Section

def help(update, context):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Get eLMIS link", callback_data='Get eLMIS link')],
                [InlineKeyboardButton("How to login?", callback_data='How to login?')],
                [InlineKeyboardButton("I don't remember my username", callback_data='I dont remember my username')],
                [InlineKeyboardButton("What should I do to change my password?", callback_data='What should I do to change my password?')],
                [InlineKeyboardButton("How to clear cache?", callback_data='How to clear cache?')],
                [InlineKeyboardButton("How do I add products?", callback_data='How do I add products?')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text("What FAQ topic do you want to view?",reply_markup=reply_markup)
    return HELP

def help_actions(update, context):
    query = update.callback_query
    if query.data == 'Get eLMIS link':
        return get_elmis_link(update, context)
    elif query.data == 'How to login?':
        return login(update, context);
    elif query.data == 'I dont remember my username':
        return forgot_username(update, context)
    elif query.data == 'How to clear cache?':
        return clear_cache_main(update, context);
    elif query.data == 'How do I add products?':
        return add_product_main(update, context)
    elif query.data == 'What should I do to change my password?':
        return change_password(update, context)
    else:
        query.message.reply_text("You requested information for <i>" + query.data + "</i>. <b>Coming soon....</b>",  parse_mode=telegram.ParseMode.HTML)
        reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
        query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
        return MAIN_MENU
    return TYPING_CHOICE


# Forgot your username
def forgot_username(update, context):
    query = update.callback_query;
    query.message.reply_text("The username the combination of the first letter of your first name with your surname, for example, <b>Hussein Hassan Matoto</b>, her username will be <b>hmatoto</b>\n" ,  parse_mode=telegram.ParseMode.HTML)
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
    return MAIN_MENU


# Change password
def change_password(update, context):
    query = update.callback_query;
    url = 'images/Password.png';
    query.message.reply_text("<b>Step 1:</b>\nGo to eLMIS homescreen\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_text("<b>Step 2:</b>\nClick forgot password.  Note even if you know your password but just need to reset it, you can use this function to reset it.\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=open(url, 'rb'))
    query.message.reply_text("<b>Step 3:</b>\nEnter your username OR email and a password reset email will be sent to you\n" ,  parse_mode=telegram.ParseMode.HTML)
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
    return MAIN_MENU

# eLMIS link
def get_elmis_link(update, context):
    query = update.callback_query
    query.message.reply_text("You can access eLIMIS through this link https://elmis.co.tz",  parse_mode=telegram.ParseMode.HTML)
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
    return MAIN_MENU

# Login Section
def login(update, context):
    query = update.callback_query
    url = 'https://api.media.atlassian.com/file/b5178612-83df-4a17-b4e7-cdcb11b2a3db/image?token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI1M2YyZjk5OC04YjIzLTQxMjYtODNkMC05YTcxY2EwNjcyNWEiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpmaWxlOmI1MTc4NjEyLTgzZGYtNGExNy1iNGU3LWNkY2IxMWIyYTNkYiI6WyJyZWFkIl19LCJleHAiOjE1NTI2NDEzNDQsIm5iZiI6MTU1MjYzODI4NH0.pKVvk8uWf0ErvXghyk2zCxgfaIzNX6WbzIOjI2ZJ7Lw&client=53f2f998-8b23-4126-83d0-9a71ca06725a&name=1219_2.png&max-age=2940&width=457&height=250';
    query.message.reply_text("<b>Step to Access your Account</b>\n\n<b>Step 1:</b>\nGo to any browser (Chrome, Mozilla, Internet Explorer etc) available at your computer and open eLMIS on your browser using this address <b>https://elmis.co.tz</b>\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=url)
    reply_markup = InlineKeyboardMarkup(next_keyboard)
    query.message.reply_text("Go to next step",reply_markup=reply_markup)
    return FILL_LOGIN_CREDENTIALS

def fill_login_credentials(update, context):
    query = update.callback_query
    url = 'https://api.media.atlassian.com/file/93f162d2-0605-4f5e-8da3-c888ee9f90f6/image?token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI1M2YyZjk5OC04YjIzLTQxMjYtODNkMC05YTcxY2EwNjcyNWEiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpmaWxlOjkzZjE2MmQyLTA2MDUtNGY1ZS04ZGEzLWM4ODhlZTlmOTBmNiI6WyJyZWFkIl19LCJleHAiOjE1NTI5MDA1NTcsIm5iZiI6MTU1Mjg5NzQ5N30.QUIamECGs8roy09mOx49ENhyJDzYvXfYQUCtbDPD_O8&client=53f2f998-8b23-4126-83d0-9a71ca06725a&name=trusted-client.png&max-age=2940&width=401&height=250';
    query.message.reply_text("<b>Step 2:</b>\nFill in your username and password and click <b>Sign in</b> button\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=url)
    reply_markup = InlineKeyboardMarkup(next_keyboard)
    query.message.reply_text("Go to next step",reply_markup=reply_markup)
    return SIGN_IN

def sign_in(update, context):
    query = update.callback_query
    url = 'https://api.media.atlassian.com/file/b7d4eb79-1385-4876-8e26-9e68f9af323b/image?token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI1M2YyZjk5OC04YjIzLTQxMjYtODNkMC05YTcxY2EwNjcyNWEiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpmaWxlOmI3ZDRlYjc5LTEzODUtNDg3Ni04ZTI2LTllNjhmOWFmMzIzYiI6WyJyZWFkIl19LCJleHAiOjE1NTI5MDA1NjAsIm5iZiI6MTU1Mjg5NzUwMH0.7y5afA96BUj3_FdETlOKKNIiCdPZzvWIR1ER8A-Py2A&client=53f2f998-8b23-4126-83d0-9a71ca06725a&name=Admin.png&max-age=2940&width=688&height=250';
    query.message.reply_text("<b>Step 3:</b>\nIf you are seeing this screen..\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=url)
    query.message.reply_text("\n..then congratulation you have successfully login into eLMIS\n" ,  parse_mode=telegram.ParseMode.HTML)
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
    return MAIN_MENU


# Clear Cache Section
def clear_cache_main(update, context):
    query = update.callback_query
    url = 'https://oit.colorado.edu/sites/default/files/tutorials/chromecache1.png';
    query.message.reply_text("<b>Steps to clear cache on Google Chrome</b>\n\n<b>Step 1:</b>\nClick the Customize and Control Chrome button on the top right side of the browser.\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=url)
    reply_markup = InlineKeyboardMarkup(next_keyboard)
    query.message.reply_text("Go to next step",reply_markup=reply_markup)
    return CLEAR_CACHE

def clear_cache(update, context):
    query = update.callback_query
    url = 'https://oit.colorado.edu/sites/default/files/tutorials/chromecache2.png';
    query.message.reply_text("<b>Step 2:</b>\nFrom the drop-down menu, hover over More Tools then select Clear Browsing Data.\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=url)
    reply_markup = InlineKeyboardMarkup(next_keyboard)
    query.message.reply_text("Go to next step",reply_markup=reply_markup)
    return CLEAR_CACHE_STEPS_TWO


def clear_cache_chrome_two(update, context):
    query = update.callback_query
    url = 'https://oit.colorado.edu/sites/default/files/tutorials/chromecache3.png';
    query.message.reply_text("<b>Step 3:</b>\nSelect the time frame you would like to delete data from the drop-down menu. Make sure the Cookies and other site data and Cached images and files checkboxes are selected. When your selections are made, click Clear browsing data.\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=url)
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
    return MAIN_MENU



# How to add product section
def add_product_main(update, context):
    query = update.callback_query
    url = 'images/products1.png';
    query.message.reply_text("All the items that are available in the msd catalog have been registered in the eLMIS. You should also remember that, some items are found in priority drugs and medical supply template while other others are in the additional"
                             " drugs and medical supply template. So, what you have to do first is to check in all  So, what you have to do first is to check in all pages of your R&R available in the eLMIS, and if you cant find it and the item is found in "
                             "the priority drug and medical supplies template, follow the subsequent steps to add ")
    query.message.reply_text("<b>Steps to clear add products on your RnR</b>\n\n<b>Step 1:</b>\nClick the add button found at the top of the right hand of your R&R.\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=open(url, 'rb'))
    reply_markup = InlineKeyboardMarkup(next_keyboard)
    query.message.reply_text("Go to next step",reply_markup=reply_markup)
    return ADD_PRODUCT

def add_product(update, context):
    query = update.callback_query
    url = 'images/products2.png'
    query.message.reply_text("<b>Step 2:</b>\nSearch the products by writing on the space or scrolling up and down to see the product.\nCheck in the product.\nClick the add selected products\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=open(url, 'rb'))
    reply_markup = InlineKeyboardMarkup(next_keyboard)
    query.message.reply_text("Go to next step",reply_markup=reply_markup)
    return ADD_PRODUCT_STEP_TWO


def add_product_step_two(update, context):
    query = update.callback_query
    url = 'images/products3.png';
    query.message.reply_text("<b>Step 3:</b>\nOn the other hand, if the item is found in the additional drugs and medical supplies then follow these steps.\n"
                             "Click the additional drugs and medical supplies template, you will the add button at the right hand of the opened template, click it\n" ,  parse_mode=telegram.ParseMode.HTML)
    query.message.reply_photo(photo=open(url, 'rb'))
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
    return MAIN_MENU

# Custom choices
def custom_choice(update, context):
    update.message.reply_text('Unknown command, sending you back to main menu')
    welcome_html_string = ('<b>Hello ' + update.message.chat.first_name.upper() + '!</b> \nWelcome to eLMIS Support Desk \n\nWhat can I help you with?')
    update.message.reply_html(welcome_html_string, reply_markup=main_menu_inline_keyboard)
    return START



# Mini Reports
def mini_reports(update, context):
    query = update.callback_query
    reply_inline = [[InlineKeyboardButton("Get RNR Status", callback_data='Get RNR Status')], [InlineKeyboardButton("Get District Reporting Rate", callback_data='Get District Reporting Rate')]]
    # main_menu_inline_keyboard = InlineKeyboardMarkup(reply_inline)
    # reply_keyboard = [['Get RNR Status','Get District Reporting Rate']]
    # markup = ReplyKeyboardMarkup(InlineKeyboardMarkup(reply_inline), one_time_keyboard=True)
    query.message.reply_text("What report would you like to see",reply_markup=InlineKeyboardMarkup(reply_inline))
    return RNR_STATUS

def get_msd_code(update, context):
    query = update.callback_query
    query.message.reply_text("Alright, what is the MSD code of your facility")
    return GET_MSD_CODE


def program_name(update, context):
    text = update.message.text
    context.user_data['facility'] = text
    reply_inline = [[InlineKeyboardButton("ILS", callback_data='ils')], [InlineKeyboardButton("ARV", callback_data='arv')], [InlineKeyboardButton("Lab System", callback_data='lab')], [InlineKeyboardButton("TB", callback_data='tb')], [InlineKeyboardButton("Redesigned ILS", callback_data='ilshosp')], [InlineKeyboardButton("Redesigned LAB", callback_data='LABReport')], [InlineKeyboardButton("Redesigned TB", callback_data='TBReport')]]
    update.message.reply_text("Choose program of your RnR",reply_markup=InlineKeyboardMarkup(reply_inline))
    return GET_PROGRAME_NAME



def getrnrstatusbyfacilitycode(update, context):
    query = update.callback_query
    text = query.data
    context.user_data['program'] = text
    user_data = context.user_data
    facility = user_data['facility']
    program = user_data['program']
    params = {'programCode' : program, 'facilityCode' : facility}
    response = requests.get(API_GET_RNR_STATUS_ENDPOINT, params = params)

    data = response.json()

    if "error" in data:
        reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
        query.message.reply_text(data["error"] + ", Go back to main menu",reply_markup=reply_markup)
        return MAIN_MENU


    status = data["requisition"]["status"]
    periodName = data["requisition"]["period"]["name"]
    periodYear = data["requisition"]["period"]["stringYear"]
    programName = data["requisition"]["program"]["name"]
    # fullSupplyItemsSubmittedCost = data["requisition"]["fullSupplyItemsSubmittedCost"]
    # nonFullSupplyItemsSubmittedCost = data["requisition"]["nonFullSupplyItemsSubmittedCost"]
    facilityName = data["requisition"]["facility"]["name"]
    facilityType = data["requisition"]["facility"]["description"]
    region = data["requisition"]["facility"]["geographicZone"]["parent"]["name"]

    bot.send_message(chat_id=query.message.chat_id,
                     text='<b>Facility Name : </b> ' + facilityName + ' ' + facilityType + ',' + region
                          + ' \n<b>Program : </b> ' + programName
                          + ' \n<b>Period : </b> ' + periodName + ' ' + periodYear
                          + ' \n<b>RnR Status : </b> ' + status
                          + ' \n<b>RnR Description : </b> ' + getdescriptionforrnrstatus(status)
                          + ' \n',
                     parse_mode=telegram.ParseMode.HTML)

    context.user_data['rnrId'] = data["requisition"]["id"]

    reply_inline = [[InlineKeyboardButton("Subscribe", callback_data='Subscribe')], [InlineKeyboardButton("Go back to Main Menu", callback_data='Go back to Main Menu')]]
    query.message.reply_text("Choose to subscribe for this RNR and get notification whenever status change or go back to main menu",reply_markup=InlineKeyboardMarkup(reply_inline))
    return SUBSCRIBE_MENU


def subscribe_menu(update, context):
    query = update.callback_query
    if query.data == 'Subscribe':
        return subscribe(update, context)
    else:
        return main_menu(update, context)


def subscribe(update, context):
    query = update.callback_query
    user_data = context.user_data
    rnrid = user_data['rnrId']

    params = {'chatId' : query.message.chat_id, 'rnrId' : rnrid, 'label': 'REQUISITION_STATUS'}
    response = requests.get(API_SUBSCRIBE, params = params)

    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("You have successfully subscribed, you will receive notification whenever status change",reply_markup=reply_markup)
    return MAIN_MENU


#coming soon
def coming_soon(update, context):
    query = update.callback_query;
    query.message.reply_text("You requested information for <i>" + query.data + "</i>. <b>Coming soon....</b>",  parse_mode=telegram.ParseMode.HTML)
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    query.message.reply_text("Go back to main menu",reply_markup=reply_markup)
    return MAIN_MENU

# Utils

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])



def getprogramcode(program):
    if program == 'ILS':
        return 'ils'
    elif program == 'ARV':
        return 'arv'
    elif program == 'TB':
        return 'tb'
    elif program == 'Lab System':
        return 'lab'
    else:
        return 'ils'


def getdescriptionforrnrstatus(rnrStatus):
    if rnrStatus == 'INITIATED':
        return 'RNR is on facility level, waiting to be submitted to facility Incharge'
    elif rnrStatus == 'SUBMITTED':
        return 'RNR is on facility level waiting for authorization from facility Incharge'
    elif rnrStatus == 'APPROVED':
        return 'RNR is on MSD level waiting to be converted to sale order'
    elif rnrStatus == 'AUTHORIZED':
        return 'RNR is on district level waiting to be approved by district pharmacist'
    elif rnrStatus == 'RELEASED':
        return 'RNR has already been converted to order'
    elif rnrStatus == 'REJECTED':
        return 'RNR has been rejected'
    elif rnrStatus == 'IN_APPROVAL':
        return 'RNR is on MSD level waiting to be converted to sale order'
    else:
        return 'Unknown status'



# RnR order status
def order_status(update, context):
     text = update.message.text
     context.user_data['facility_code'] = text
     reply_keyboard = [['ILS', 'ARV', 'TB']]
     markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
     update.message.reply_text("You want to know status of what program?",reply_markup=markup)
     return ORDER_STATUS_PROGRAM

def order_status_program(update, context):
     text = update.message.text
     update.message.reply_text("Your R&R for Progam X is ....")
     reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
     update.message.reply_text("Go back to main menu",reply_markup=reply_markup)
     return MAIN_MENU

# Reporting rate

def district_reporting_rate(update, context):
    text = update.message.text
    context.user_data['district_name'] = text
    reply_keyboard = [['ILS', 'ARV', 'TB']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("You want to know status of what program?", reply_markup=markup)
    return DISTRICT_REPORTING_RATE_PROGRAM

def district_reporting_rate_program(update, context):
     text = update.message.text
     update.message.reply_text("Reporting Rate is ....")
     reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
     update.message.reply_text("Go back to main menu",reply_markup=reply_markup)
     return MAIN_MENU




def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("711948397:AAF1NNp3m1uWkcCyttkGVVQd21UzQakIfRg", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^Help/FAQ$',
                                    help,
                                    pass_user_data=True),
                      RegexHandler('^Mini Reports$',
                                   mini_reports,
                                    pass_user_data=True),
                       RegexHandler('^Get RNR Status$',
                                    get_msd_code,
                                    pass_user_data=True),
                       RegexHandler('^Subscribe$', subscribe, pass_user_data=True),
                       RegexHandler('^Go back to Main Menu', start, pass_user_data=True),
                       RegexHandler('^Get District Reporting Rate', coming_soon, pass_user_data=True)
                       ],
            MAIN_MENU: [CallbackQueryHandler(
                                          main_menu,
                                          pass_chat_data=True),
                       ],
              START: [CallbackQueryHandler(start_menu, pass_chat_data=True),],
              HELP: [CallbackQueryHandler(help_actions, pass_chat_data=True),
                           ],
              FILL_LOGIN_CREDENTIALS: [CallbackQueryHandler(
                                        fill_login_credentials,
                                          pass_chat_data=True),
                           ],
              SIGN_IN: [CallbackQueryHandler(
                                          sign_in,
                                          pass_chat_data=True),
                           ],
              CLEAR_CACHE: [CallbackQueryHandler(
                                          clear_cache,
                                          pass_chat_data=True),
                           ],
              CLEAR_CACHE_STEPS_TWO: [CallbackQueryHandler(
                                          clear_cache_chrome_two,
                                          pass_chat_data=True),
                           ],
            ADD_PRODUCT: [CallbackQueryHandler(
                                          add_product,
                                          pass_user_data=True),
                           ],
            ADD_PRODUCT_STEP_TWO: [CallbackQueryHandler(
                                          add_product_step_two,
                                          pass_chat_data=True),
                           ], 
              DISTRICT_REPORTING_RATE: [MessageHandler(Filters.text,
                                          district_reporting_rate,
                                          pass_user_data=True),
                           ],
              DISTRICT_REPORTING_RATE_PROGRAM: [MessageHandler(Filters.text,
                                          district_reporting_rate_program,
                                          pass_user_data=True),
                           ],
            GET_MSD_CODE: [MessageHandler(Filters.text,
                program_name,
                pass_chat_data=True),
          ],
            GET_PROGRAME_NAME:[CallbackQueryHandler(
               getrnrstatusbyfacilitycode,
        pass_chat_data=True),
                ],
            MIN_REPORT:[CallbackQueryHandler(
                get_msd_code,
                pass_chat_data=True),
            ],
            COMING_SOON: [CallbackQueryHandler(
                coming_soon,
                pass_chat_data=True),

            ],
            RNR_STATUS: [CallbackQueryHandler(
                 get_msd_code,
                 pass_chat_data=True)],
            SUBSCRIBE_MENU : [CallbackQueryHandler(
                subscribe_menu,
                pass_chat_data=True)]
        },

        fallbacks=[RegexHandler('^Shit', main_menu),
                   CommandHandler('help', main_menu)]
    )


    dp.add_handler(conv_handler)


    # log all errors
    dp.add_error_handler(custom_choice)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()