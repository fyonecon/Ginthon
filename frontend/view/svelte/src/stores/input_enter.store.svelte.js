// 判断输入法是否正确完成输入并Enter
export const input_enter_data = $state({
    input_doing: 1, // 判断用户输入框是否已经输入完成。 1直接完成输入，2预选词输入完成，-1开始输入，0词预选状态。1和2都是输入完成，请区分具体数值。
});