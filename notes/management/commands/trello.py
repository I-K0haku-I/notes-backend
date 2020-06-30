from trello import Webhooks, Boards, TrelloApi
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true')

    def handle(self, *args, **options):
        trello = TrelloApi(settings.TRELLO_KEY, settings.TRELLO_TOKEN)
        boards = trello.members.get_board(settings.TRELLO_USER)
        for i, board in enumerate(boards):
            print(str(i).ljust(3), board['name'].ljust(40), '|', board['id'])
        selected = int(input())
        board_id = boards[selected]['id']
        
        if options['delete']:
            data_list = trello.members.get_token(settings.TRELLO_USER, webhooks='true')
            wh_id = None
            if data_list:
                webhooks_list = data_list[0]['webhooks']
                for wh in webhooks_list:
                    if wh['idModel'] == board_id:
                        wh_id = wh['id']
                        break
            print('Deleting webhook for:', wh_id)
            trello.webhooks.delete(wh_id)
        else:
            r = trello.webhooks.new(settings.TRELLO_CALLBACK, board_id, description='Tets')
            print('Selected board will now call this endpoint after changes:')
            print(settings.TRELLO_CALLBACK)
            print(board_id)
            print(r)
        