import numpy as np

# Implements the stationary bootstrap for bootstrapping stationary, dependent series
# 
# USAGE:
#   [BSDATA, INDICES] = stationary_bootstrap(DATA,B,W)
# 
# INPUTS:
#   DATA   - T by 1 vector of data to be bootstrapped
#   B      - Number of bootstraps
#   W      - Average block length. P, the probability of starting a new block is defined P=1/W
# 
# OUTPUTS:
#   BSDATA  - T by B matrix of bootstrapped data
#   INDICES - T by B matrix of locations of the original BSDATA=DATA(indexes);
# 
# COMMENTS:
#   To generate bootstrap sequences for other uses, such as bootstrapping vector processes,
#   set DATA to (1:N)'.  
#
# See also block_bootstrap

#  Implements the stationary bootstrap for bootstrapping stationary, dependent series
#  From 
#  Author: Kevin Sheppard
#  kevin.sheppard@economics.ox.ac.uk
#  Revision: 2    Date: 12/31/2001
#
#  Modified from Matlab to Python - 05/12/2016
#  Florent Brient
#  florent.brient@gmail.com



def stat_boot(data,B,w) :

  t = data.shape[0]
  # Some input checking 
  if len(data.shape) > 1 :
    sys.exit('DATA must be a column vector')
  if data.shape < 2 :
    sys.exit('DATA must have at least 2 observations.')
  if not np.isscalar(w) or w<=0:
    sys.exit('W must be a positive scalar.')
  if not np.isscalar(B) or B<1 or np.floor(B)!=B:
    sys.exit('B must be a positive scalar integer')


  # Define the probability of a new block
  p = 1/float(w)
  # Set up the bsdata and indices
  indices = np.zeros((t,B))
  # Initial position
  indices[0,:]=np.ceil(t*np.random.random(B))-1
  # Set up the random numbers
  select          = np.random.random((t,B))<p
  indices[select] = np.ceil(t*np.random.random(sum(sum(select))))-1
  for i in np.arange(1,t):
    # Determine whether we stay (rand>p) or move to a new starting value
    # (rand<p)
    indices[i,~select[i,:]]=indices[i-1,~select[i,:]]+1

  # Move extra indexes out of the time boundaries to the first positions
  indices[indices>=t] = indices[indices>=t]-t

  # Make integer of indexes
  indices = indices.astype(int)
  # The indices make finding the bsdata simple
  bsdata = data[indices]

  return bsdata, indices
  
  
  