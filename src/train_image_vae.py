import utils
from data_loader import DataLoader, ImageDataset
from params import Params
from vae_lp import VAE_LP


args = Params().parse()

args.image_dir = "../data/Generalv1/image/"
args.vae_dir = "../output/Generalv1VAE_256/"
args.vae_dim = 256

args.image_root = args.vae_dir + 'image/'
args.ckpt_root = args.vae_dir + 'ckpt/'

utils.make_path(args.image_root)
utils.make_path(args.image_root + 'train/')
utils.make_path(args.image_root + 'test/')
utils.make_path(args.ckpt_root)

data_loader = DataLoader(args)
vae = VAE_LP(args)

train_dataset = ImageDataset(args, split='train')
test_dataset = ImageDataset(args, split='test')

train_loader = data_loader.get_loader(train_dataset)
test_loader = data_loader.get_loader(test_dataset, shuffle=False)

for i in range(args.vae_epoch):
    vae.train(train_loader)
    if i % args.test_freq == 0:
        vae.test(test_loader)
        vae.save_model('%s/ckpt/%03d.pth' % (args.vae_dir, i))

# vae.load_model(args.ckpt_root + "095.pth")
# output = vae.generate()
# utils.save_image(output, (args.image_root + 'generate.jpg'), normalize=True)
