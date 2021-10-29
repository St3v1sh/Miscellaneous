/**
 * This code will continuously cycle through your Discord voice channels. The
 * voice channels must always be in view or the website will unload the
 * buttons.
 * 
 * @author  sky3947@rit.edu
 * @since   10.29.2021
 */

const VOICE_CHANNEL = '(voice channel)';

let running = true;
let counter = -1;
let timeout = 2000;
let exclude = ['Shhhhh, Napping', 'Screaming into the Void'];
let voiceChannels;
exclude = exclude.map(nom => `${nom} ${VOICE_CHANNEL}`);

const arrIncludes = (str, arr) => {
  let flag = false
  arr.forEach(elm => {
    if(str.includes(elm)) flag = true
  })
  return flag
}

const switching = () => {
  setTimeout(() => {
    voiceChannels = Array.from(document.getElementsByTagName('a')).filter(chan => chan.outerHTML.includes(VOICE_CHANNEL));
    voiceChannels = voiceChannels.filter(chan => !(arrIncludes(chan.outerHTML, exclude)))
    if (running && voiceChannels.length > 0) {
      counter = (counter + 1) % voiceChannels.length;
      voiceChannels[counter].click();
      switching();
    } else {
      running = true;
    }
  }, timeout);
}
switching();
