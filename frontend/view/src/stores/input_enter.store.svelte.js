// 判断输入法是否正确完成输入并Enter
export const input_enter_data = $state({
    input_doing: 10, // 默认10。10字母数字输入开始，12字母数字输入完成；20汉字开始输入，21汉字预选词状态，22汉字输入完成。请区分具体数值。
});