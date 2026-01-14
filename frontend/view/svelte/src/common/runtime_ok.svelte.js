/**
 *  page运行时检测，拦截爬虫、审核等
 * @returns {boolean} 返回固定格式
 */
export const runtime_ok = function (){
    let inner_w = window.innerWidth;
    let inner_h = window.innerHeight;
    let screen_w = window.screen.width;
    let screen_h = window.screen.height;
    return !(inner_w < 220 || inner_h < 220 || screen_w < 220 || screen_h < 220 || navigator.webdriver || !window.localStorage || !window.indexedDB);
}