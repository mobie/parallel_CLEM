import mobie

def add_em_volume():
    path1 = 'data/MSB30_4/images/bdv-n5/MSB30_4.xml'
    mobie.add_bdv_image(path1, './data', 'MSB30_4', image_name='MSB30_4', menu_name='EM', move_data=True)

if __name__ == '__main__':
    add_em_volume()