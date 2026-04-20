<script>
    import {alert_data} from "../stores/alert.store.svelte.js"
</script>

<div class="alert_loading-div select-none {alert_data.alert_show}">
    <div class="select-none">
        <div class="loading-info ">
            <div class="alert_loading_msg break border-radius font-text bg-neutral-200 dark:bg-neutral-900 select-text">{alert_data.alert_msg}</div>
        </div>
    </div>
</div>

<style>
    .alert_loading-div{
        position: fixed;
        z-index: 100;
        width: 100%;
        height: 100%;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: auto auto;
        background-color: rgba(50, 50, 50, 0);
    }
    .loading-info{
        position: absolute;
        width: 280px;
        max-height: 180px;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: auto auto;
        text-align: center;
    }
    .alert_loading_msg{
        text-align: center;
        width: 280px;
        line-height: 22px;
        max-height: 108px;
        overflow: hidden;
        margin-bottom: 10px;
        padding: 10px 10px;
        box-shadow: 0 0 40px rgba(150, 150, 150, 0.2);
    }

</style>