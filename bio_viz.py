import matplotlib as mpl
from matplotlib import pyplot as plt

plt.style.use('seaborn-ticks')
from matplotlib import transforms
import matplotlib.patheffects
from matplotlib.font_manager import FontProperties
from bio_encoding import encode_strings

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
  

class Scale(matplotlib.patheffects.RendererBase):
  def __init__(self, sx, sy=None):
    self._sx = sx
    self._sy = sy

  def draw_path(self, renderer, gc, tpath, affine, rgbFace):
    affine = affine.identity().scale(self._sx, self._sy)+affine
    renderer.draw_path(gc, tpath, affine, rgbFace)

def draw_motif_logo(motif, fontfamily='Arial', size=80, start_ind=0, end_ind=None, x_offset=0):
  bps = len(motif.pwm['A'])
  if end_ind is None:
    end_ind = bps
  scores = []
  for i in range(start_ind, end_ind):
    scores.append([(k, motif.pwm[k][i]) for k in ['A', 'G', 'C', 'T']])
  draw_logo(scores, fontfamily=fontfamily, size=size, x_offset=x_offset)

def print_snp_flankingseq(dna):
  if type(dna) == np.ndarray:
    dna = encode_strings(dna)
  print(dna[:499] + color.RED + color.BOLD + dna[499] + color.END\
        + color.BLUE + dna[500:] + color.END)

def draw_logo(all_scores, fontfamily='Arial', size=80, x_offset=0):
  """
  Taken from http://nbviewer.jupyter.org/github/saketkc/notebooks/blob/master/python/Sequence%20Logo%20Python%20%20--%20Any%20font.ipynb?flush=true
  discussion thread here https://github.com/biopython/biopython/issues/850

  all_scores is a list of lists of tuples, with each list containing
  tuples of the form ('C', 0.034) giving the scores for that base pair.

  These letter-scores for a given base pair do not need to be provided in any particular order
  """
  if fontfamily == 'xkcd':
      plt.xkcd()
  else:
      mpl.rcParams['font.family'] = fontfamily

  fig, ax = plt.subplots(figsize=(len(all_scores), 2.5))

  font = FontProperties()
  font.set_size(size)
  font.set_weight('bold')
  
  #font.set_family(fontfamily)

  ax.set_xticks(range(x_offset+1,len(all_scores)+1))    
  ax.set_yticks(range(0,3))
  ax.set_xticklabels(range(1,len(all_scores)+1), rotation=90)
  ax.set_yticklabels(np.arange(0,3,1))    
  seaborn.despine(ax=ax, trim=True)
  
  trans_offset = transforms.offset_copy(ax.transData, 
                                        fig=fig, 
                                        x=1, 
                                        y=0, 
                                        units='dots')
 
  for index, scores in enumerate(all_scores):
      yshift = 0
      for base, score in scores:
          txt = ax.text(x_offset+index+1, 
                        0, 
                        base, 
                        transform=trans_offset,
                        fontsize=80, 
                        color=COLOR_SCHEME[base],
                        ha='center',
                        fontproperties=font,

                       )
          txt.set_path_effects([Scale(1.0, score)])
          fig.canvas.draw()
          window_ext = txt.get_window_extent(txt._renderer)
          yshift = window_ext.height*score
          trans_offset = transforms.offset_copy(txt._transform, 
                                                fig=fig,
                                                y=yshift,
                                                units='points')
      trans_offset = transforms.offset_copy(ax.transData, 
                                            fig=fig, 
                                            x=1, 
                                            y=0, 
                                            units='points')    
  plt.show()
