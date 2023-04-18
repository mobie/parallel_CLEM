import mobie

def add_segmentation():
    path = '/g/kreshuk/pape/Work/data/mobie/mobie-example-data/em_segmentation.tif'

    resolution = [2., 0.03, 0.03]
    chunks = [1, 256, 256]
    scale_factors = [[1, 2, 2], [1, 2, 2], [1, 2, 2], [1, 2, 2]]

    mobie.add_segmentation(path, '', root='./data', dataset_name='yeast',
                           segmentation_name='em-segmentation',
                           resolution=resolution, scale_factors=scale_factors,
                           chunks=chunks, unit='micrometer')


if __name__ == '__main__':
    add_segmentation()