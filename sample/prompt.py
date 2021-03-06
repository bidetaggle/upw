import getpass, os, sys, clipboard
from sample import upw, cfg, password, lib
from .User import User
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

def identify():

    print('- 1. Identification -\n')
    print('Make sure to cover your keyboard from any camera,')
    print('window and any potential eavesdropper.\n')

    Login = input("* Login: ")
    MasterPassword = getpass.getpass(prompt='* Master Password: ', stream = None)
    user = User(Login, MasterPassword)
    MasterPassword = None # Make sure Master Password typed by the user is no longer in memory

    print('\nEmojish: *** [ ' + user.emojish + ' ] ***')
    return user
    # DEBUG:
    # return User('user name', 'masterpassword')

def create(user):
    print('\n* Please confirm the master password you typed')
    print('  before.\n')
    print('* login: ' + user.login)
    MasterPasswordConfirmation = getpass.getpass(prompt='* Master Password: ', stream = None)
    # if(upw.authenticate(user['login'], MasterPasswordConfirmation)['hash'] == user['hash']):
    if(User(user.login, MasterPasswordConfirmation).hash == user.hash):
        user.create()
        print('\n*** High five ' + user.login + '! ***\n')
        print('* Your encrypted profile has been created:')
        print('\n ' + cfg.get('UPW_DIR') + user.hash + '\n')
    else:
        print('\n* The password doesn\'t match with the first\n  typed in.\n')
        sys.exit(0)

def authenticate(user):

    print('\n- 2. Authentication -\n')
    print('\nEmojish: *** [ ' + user.emojish + ' ] ***\n\n')

    # Is this user has a file in .upw/ ?
    if(user.import_profile()):
        print('* A matching profile has been found: ')
        print('\n ' + cfg.get('UPW_DIR') + user.hash)
        print()

    else:
        print('-------------- Welcome to μPassword -------------')
        print('***                                           ***')
        print('***           You are about to create         ***')
        print('***      a new login/master password pair     ***')
        print('***                                           ***')
        print('-------------------------------------------------')
        print()
        print('* If this is what you want, type `confirm` below')
        print()
        print('* If you\'re trying to authenticate with a login')
        print('  you\'ve already made before on this device, you')
        print('  likely mistyped your master password.')
        print('  Just press [Enter] :)')
        print()
        if(input('> ') == 'confirm'):
            create(user)
        else:
            sys.exit(0)

def options():
    os.system('clear')
    print('-------------- μPassword: options ---------------')
    print('***                                           ***')
    print('***             Work in progress              ***')
    print('***                     :)                    ***')
    print('***                                           ***')
    print('-------------------------------------------------')
    input('\n-> Press enter to continue...')

def select_domain(user):
    while 1:
        os.system('clear')
        print('-> Type `options` to access your profile options.\n')
        domain = prompt('[ ' + user.emojish + ' ] <' + user.login + '> Domain: ',
            completer=WordCompleter(user.get_domains())
            # history=FileHistory(cfg.get('UPW_DIR') + 'history.txt'),
            # auto_suggest=AutoSuggestFromHistory(),
            )
        if(domain == 'options'):
            options()
        else:
            clipboard.copy(password.generate(user.masterkey, domain))
            print('\n*** Copied to clipboard. ***\n')
            if(user.add_domain(domain)):
                print('This domain has been added to your profile!\n')
            print('-> Type `delete` to remove ' + domain + ' from your profile.')
            print('-> Press enter to continue.')
            keypress = input()
            if(keypress == 'delete'):
                print('profile deleted')
