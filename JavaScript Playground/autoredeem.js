/**
 * This code will automatically redeem points rewards on twtich.tv. The target
 * redeem is in the constant `TARGET_REDEEM`. Change `maxIterations` to the
 * desired number of redeems. Don't forget to un-comment `btnConfirm.click();`!
 * This code also assumes that the target redeem has no cooldown.
 *
 * @author  sky3947@rit.edu
 * @since   1.18.2023
 */

let TARGET_REDEEM = 'Hydrate';

let getOpenRedeemsMenuButton = () => document.querySelector('[aria-label="Bits and Points Balances"]');
let getRedeemButton = () => document.querySelector(`[title="${TARGET_REDEEM}"]`).parentElement.parentElement.firstChild;
let getConfirmButton = () => document.querySelector('[data-test-selector="RewardText"]').parentNode.parentElement.parentElement.parentElement;

let iteration = 0;
let maxIterations = 1;
const q = () => iteration = maxIterations;

const States = {
  INITIAL: 0,
  WAITING_FOR_REDEEM_BUTTON: 1,
  WAITING_FOR_CONFIRM_BUTTON: 2,
};
const nextState = (state) => (state + 1) % Object.keys(States).length;

const autoClick = (state) => {
  if (iteration >= maxIterations) return;

  switch (state) {
    case States.INITIAL:
      console.log('Emergency stop: use `q()` to stop\nopening rewards div');
      if (getOpenRedeemsMenuButton() === null) {
        autoClicker(state);
        return;
      }

      getOpenRedeemsMenuButton().click();
      autoClicker(nextState(state));
      return;

    case States.WAITING_FOR_REDEEM_BUTTON:
      console.log(`waiting for redeem button "${TARGET_REDEEM}"`);
      if (getRedeemButton() === null) {
        autoClicker(state);
        return;
      }

      getRedeemButton().click();
      autoClicker(nextState(state));
      return;

    case States.WAITING_FOR_CONFIRM_BUTTON:
      console.log('waiting for confirm redeem button');
      if (getConfirmButton() === null) {
        autoClicker(state);
        return;
      }

      // getConfirmButton().click();
      getOpenRedeemsMenuButton().click();
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
