/**
 * This code will automatically redeem points rewards on twtich.tv. The target
 * redeem is in the constant `TARGET_REDEEM`. Change `maxIterations` to the
 * desired number of redeems. Don't forget to un-comment `btnConfirm.click();`!
 * This code also assumes that the target redeem has no cooldown.
 * 
 * @author  sky3947@rit.edu
 * @since   10.29.2021
 */

const TARGET_REDEEM = 'Hydrate';

const REDEEMS_CLASS_NAME = 'Layout-sc-nxg1ff-0 cmslTX';
const CONFIRM_BUTTONS_CLASS_NAME = 'Layout-sc-nxg1ff-0 hClGgz';

const $className = (className) => document.getElementsByClassName(className);
const $qSelectorAll = (query) => document.querySelectorAll(query);

let btnOpenRedeems = $qSelectorAll('[aria-label="Points Balance"]')[0];
let btnRedeem;
let btnConfirm;

let iteration = 0;
let maxIterations = 1;
const q = () => iteration = maxIterations;

const States = {
  INITIAL: 0,
  WAITING_FOR_REDEEM_BUTTON: 1,
  WAITING_FOR_CONFIRM_BUTTON: 2,
};
const nextState = (state) => (state+1) % Object.keys(States).length;

const autoClick = (state) => {
  if(iteration >= maxIterations) return;
  
  switch(state) {
    case States.INITIAL:
      console.log('Emergency stop: use `q()` to stop\nopening rewards div');
      if($className(REDEEMS_CLASS_NAME).length > 0) {
        autoClicker(state);
        return;
      }
      
      btnOpenRedeems.click();
      autoClicker(nextState(state));
      return;
      
    case States.WAITING_FOR_REDEEM_BUTTON:
      console.log(`waiting for redeem button "${TARGET_REDEEM}"`);
      let redeems = Array.from($className(REDEEMS_CLASS_NAME));
      redeems = redeems.filter(redeem => redeem.children.length > 1 && redeem.children[1].innerText === TARGET_REDEEM);
      if(redeems.length === 0) {
        autoClicker(state);
        return;
      }
      
      btnRedeem = redeems[0].children[0];
      btnRedeem.click();
      autoClicker(nextState(state));
      return;
      
    case States.WAITING_FOR_CONFIRM_BUTTON:
      console.log('waiting for confirm redeem button');
      let confirmButtonsDivs = $className(CONFIRM_BUTTONS_CLASS_NAME);
      if(confirmButtonsDivs.length === 0) {
        autoClicker(state);
        return;
      }
      
      let confirmButtons = Array.from(confirmButtonsDivs).filter(elm => elm.innerHTML.includes('>Redeem<'));
      if(confirmButtons.length === 0) {
        autoClicker(state);
        return;
      }
      
      btnConfirm = confirmButtons[0].children[0];
      // btnConfirm.click();
      iteration++;
      autoClicker(nextState(state));
      return;
      
    default:
      console.error('Error: Invalid state');
  }
};

const autoClicker = (state) => setTimeout(() => autoClick(state), 1);

const startAutoClicker = () => {
  iteration = 0;
  autoClicker(States.INITIAL);
};
startAutoClicker();