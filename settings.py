world_map = [   
    '                                                                  ',
    '                                                                  ',
    '              t  t                                                ',
    '       X     XXXXXXXXXs                   XX   X                  ',
    ' tXXXt     XX         XX                XXXD tt DX                ',
    ' XD DX                                      XXXXX                 ',
    '          Xt    t           t  t   X                            G ',
    '        XXXXXX  XXXXs    XXXXXXXXXXX  XX              tt t     XXX',
    ' P   XX  D DD D  D DDXt     X DD  DD  DDX  XXXXXXXXs  XXXXXX      ',
    'XXXXXDD  D  D D  D  DDXXXXXXD DD  DD  DDD  DD DD DDDDDDD  D       ',
]

## " " - заготовка b. "X" - блоки поверхности. "D" - блоки земли. "W" - невидимая стена. "s" - пилы / лезвия (ловушки). "P" - Имя игрока. "G" - цель, которую нужно достичь, чтобы завершить игровое задание.

tile_size = 50
WIDTH, HEIGHT = 700, len(world_map) * tile_size
