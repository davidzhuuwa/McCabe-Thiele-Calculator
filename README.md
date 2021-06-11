# McCabe Thiele Calculator
 Repository for code to calculate the number of McCabe Thiele stages expected for a distillation column given user inputs. 
 Potential to be extended to a website in the future using an appropriate Python framework. 
 
## Running the code
Running the code is as simple as typing "python mccabe.py" in the command window. A basic tkinter GUI will then pop up, prompting for feed quality, reflux ratio, 
relative volatility, and feed, tops and bottom compositions. Once these are entered, the number of theoretical stages is calculated. 
A plot of the McCabe Thiele diagram at this stage will only appear if the code is run in a Jupyter interactive window. 

## Further details
 
Assumptions in the calculator include:
1. Equilibrium Reboiler
2. Total Condenser
3. Constant Relative Volatility
4. Constant Molal Overflow
5. Binary Mixture

The calculator will eventually include code to calculate:

1. Stage compositions
2. Minimum reflux ratio (Underwood); and
3. Minimum number of theoretical plates (Fenske)

Any other suggested features are most welcome. 
