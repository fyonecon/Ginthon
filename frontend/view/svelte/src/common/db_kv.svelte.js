import Dexie from "dexie";

// kv型indexDB数据库
const kv_db_name = "dexie_kv_db";
let DexieKVDB = $state();
let isInitialized = $state(false);
/*
let data_dict_array = [
    {
        only_key: "test",
        any_type_value: {"test": 2025},
        update_time: that.get_time_s_date("YmdHis"),  // 使用时间戳
        remark: "测试",
    }
];
* */
//
const dexie_kv_db = {
    // 初始化数据库
    init_db: async function () {
        if (DexieKVDB && isInitialized) {
            return DexieKVDB;
        }

        try {
            DexieKVDB = new Dexie(kv_db_name);
            DexieKVDB.version(1).stores({
                items: '++id, &only_key, any_type_value, update_time, remark'
            });

            await DexieKVDB.open();
            isInitialized = true;
            return DexieKVDB;
        } catch (error) {
            console.error("数据库初始化失败:", error);
            throw error;
        }
    },

    // 确保数据库已初始化
    ensureDB: async function () {
        if (!DexieKVDB || !isInitialized) {
            return await this.init_db();
        }
        return DexieKVDB;
    },

    // 获取格式化日期时间
    get_time_s_date: function(format, time_s = "") {
        let t;
        if (!time_s) {
            t = new Date();
        } else {
            // 处理时间戳（支持字符串和数字）
            t = new Date(typeof time_s === 'number' ? time_s : parseInt(time_s, 10));
        }

        // 验证日期有效性
        if (isNaN(t.getTime())) {
            t = new Date();
        }

        let seconds = t.getSeconds();
        let minutes = t.getMinutes();
        let hour = t.getHours();
        let day = t.getDate();
        let month = t.getMonth() + 1;
        let year = t.getFullYear();
        let week = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][t.getDay()];

        // 补零
        seconds = seconds < 10 ? "0" + seconds : seconds;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        hour = hour < 10 ? "0" + hour : hour;
        day = day < 10 ? "0" + day : day;
        month = month < 10 ? "0" + month : month;

        // 替换格式化字符
        let result = format;
        result = result.replaceAll("Y", year);
        result = result.replaceAll("m", month);
        result = result.replaceAll("d", day);
        result = result.replaceAll("H", hour);
        result = result.replaceAll("i", minutes);
        result = result.replaceAll("s", seconds);
        result = result.replaceAll("W", week);

        return result*1;  // 返回格式化字符串
    },

    // 测试数据库
    test_db: async function () {
        let that = this;
        //
        try {
            let data_dict_array = [
                {
                    only_key: "test",
                    any_type_value: {"test": 2025},
                    update_time: that.get_time_s_date("YmdHis"),  // 使用时间戳
                    remark: "测试",
                }
            ];
            const ids_array = await this.update_db_data(data_dict_array);  // 添加 await
            console.log("测试数据插入成功, IDs:", ids_array);
            return ids_array;
        } catch (error) {
            console.error("测试失败:", error);
            return [];
        }
    },

    // 更新/插入数据
    update_db_data: async function (data_dict_array = []) {
        let that = this;
        //
        if (!Array.isArray(data_dict_array) || data_dict_array.length === 0) {
            console.warn("要存储的数据格式不正确或为空");
            return [];
        }

        try {
            const db = await this.ensureDB();
            const ids_array = [];

            await db.transaction('rw', db.items, async () => {
                for (const item of data_dict_array) {
                    if (!item.only_key || item.only_key.indexOf("%") !== -1 || item.only_key.indexOf("&") !== -1 || item.only_key.indexOf("^") !== -1 || item.only_key.indexOf("$") !== -1 || item.only_key.indexOf("!") !== -1) {
                        console.warn("only_key缺失或含有非法字符, 跳过:", item);
                        continue;
                    }

                    // 检查是否已存在
                    const existing = await db.items
                        .where('only_key')
                        .equals(item.only_key)
                        .first();

                    const currentTime = that.get_time_s_date("YmdHis");  // 使用时间戳

                    if (existing) {
                        // 更新现有记录
                        await db.items.update(existing.id, {
                            any_type_value: item.any_type_value,
                            update_time: currentTime,  // 更新时间戳
                            remark: item.remark !== undefined ? item.remark : existing.remark
                        });
                        ids_array.push(existing.id);
                        // console.log(`更新记录: ${item.only_key}, ID: ${existing.id}`);
                    } else {
                        // 添加新记录
                        const itemWithTime = {
                            only_key: item.only_key,
                            any_type_value: item.any_type_value,
                            update_time: item.update_time || currentTime,  // 使用传入的或当前时间
                            remark: item.remark || ""
                        };
                        const id = await db.items.add(itemWithTime);
                        ids_array.push(id);
                        // console.log(`新增记录: ${item.only_key}, ID: ${id}`);
                    }
                }
            });

            return ids_array;
        } catch (error) {
            console.error("更新数据失败:", error);
            return [];
        }
    },

    // 获取单条数据
    get_db_data: async function (only_key = "test") {
        if (only_key.indexOf("%") !== -1 || only_key.indexOf("&") !== -1 || only_key.indexOf("^") !== -1 || only_key.indexOf("$") !== -1 || only_key.indexOf("!") !== -1){
            console.warn("only_key含有非法字符:", only_key);
            return null;
        }
        try {
            const db = await this.ensureDB();
            const items = await db.items
                .where("only_key")
                .equals(only_key)
                .toArray();

            return items.length > 0 ? items[0] : null;
        } catch (error) {
            console.error("查询数据失败:", error);
            return null;
        }
    },

    // 查询前缀匹配的数据
    get_has_prefix_key_db_datas: async function (prefix_key = "test") {
        if (prefix_key.indexOf("%") !== -1 || prefix_key.indexOf("&") !== -1 || prefix_key.indexOf("^") !== -1 || prefix_key.indexOf("$") !== -1 || prefix_key.indexOf("!") !== -1){
            console.warn("only_key含有非法字符:", prefix_key);
            return [];
        }
        try {
            const db = await this.ensureDB();
            return await db.items
                .where("only_key")
                .startsWith(prefix_key)
                .toArray();
        } catch (error) {
            console.error("查询前缀数据失败:", error);
            return [];
        }
    },

    // 查询包含某个字符的数据
    get_contains_key_db_datas: async function (search_text = "") {
        if (search_text.indexOf("%") !== -1 || search_text.indexOf("&") !== -1 || search_text.indexOf("^") !== -1 || search_text.indexOf("$") !== -1 || search_text.indexOf("!") !== -1){
            console.warn("only_key含有非法字符:", search_text);
            return [];
        }
        try {
            const db = await this.ensureDB();
            // 由于Dexie没有直接的contains方法，需要全表扫描
            const allItems = await db.items.toArray();
            return allItems.filter(item =>
                item.only_key && item.only_key.includes(search_text)
            );
        } catch (error) {
            console.error("查询包含字符的数据失败:", error);
            return [];
        }
    },

    // 删除单条数据
    del_db_data: async function (only_key = "test") {
        if (only_key.indexOf("%") !== -1 || only_key.indexOf("&") !== -1 || only_key.indexOf("^") !== -1 || only_key.indexOf("$") !== -1 || only_key.indexOf("!") !== -1){
            console.warn("only_key含有非法字符:", only_key);
            return false;
        }
        try {
            const db = await this.ensureDB();
            const deletedCount = await db.items
                .where("only_key")
                .equals(only_key)
                .delete();

            return deletedCount > 0;
        } catch (error) {
            console.error("删除数据失败:", error);
            return false;
        }
    },

    // 删除时间段内的数据
    del_timeout_db_datas: async function (start_time, end_time) {
        if (!start_time || !end_time) {
            console.warn("请提供有效的时间范围");
            return 0;
        }

        try {
            const db = await this.ensureDB();
            const start = Number(start_time);
            const end = Number(end_time);

            if (isNaN(start) || isNaN(end)) {
                console.warn("时间参数无效");
                return 0;
            }

            const deletedCount = await db.items
                .where("update_time")
                .between(start, end)
                .delete();

            return deletedCount;
        } catch (error) {
            console.error("删除时间段数据失败:", error);
            return 0;
        }
    },

    // 删除前缀匹配的数据
    del_has_prefix_key_db_datas: async function (prefix_key = "test") {
        if (prefix_key.indexOf("%") !== -1 || prefix_key.indexOf("&") !== -1 || prefix_key.indexOf("^") !== -1 || prefix_key.indexOf("$") !== -1 || prefix_key.indexOf("!") !== -1){
            console.warn("only_key含有非法字符:", prefix_key);
            return 0;
        }
        try {
            const db = await this.ensureDB();
            const deletedCount = await db.items
                .where("only_key")
                .startsWith(prefix_key)
                .delete();

            return deletedCount;
        } catch (error) {
            console.error("删除前缀数据失败:", error);
            return 0;
        }
    },

    // 获取所有数据
    get_all_db_data: async function () {
        try {
            const db = await this.ensureDB();
            return await db.items.toArray();
        } catch (error) {
            console.error("获取所有数据失败:", error);
            return [];
        }
    },

    // 统计数据数量
    get_db_data_count: async function () {
        try {
            const db = await this.ensureDB();
            return await db.items.count();
        } catch (error) {
            console.error("统计数据数量失败:", error);
            return 0;
        }
    },

    // 批量删除多个key
    del_many_db_data: async function (keys = []) {
        try {
            const db = await this.ensureDB();
            let deletedTotal = 0;

            await db.transaction('rw', db.items, async () => {
                for (const only_key of keys) {
                    if (only_key.indexOf("%") !== -1 || only_key.indexOf("&") !== -1 || only_key.indexOf("^") !== -1 || only_key.indexOf("$") !== -1 || only_key.indexOf("!") !== -1){
                        console.warn("only_key含有非法字符:", only_key);
                        continue;
                    }
                    const deletedCount = await db.items
                        .where("only_key")
                        .equals(only_key)
                        .delete();
                    deletedTotal += deletedCount;
                }
            });

            return deletedTotal;
        } catch (error) {
            console.error("批量删除数据失败:", error);
            return 0;
        }
    },

    // 关闭数据库
    close_db: async function () {
        if (DexieKVDB && isInitialized) {
            try {
                await DexieKVDB.close();
                DexieKVDB = null;
                isInitialized = false;
            } catch (error) {
                console.error("关闭数据库失败:", error);
            }
        }
    }
};

export default dexie_kv_db;