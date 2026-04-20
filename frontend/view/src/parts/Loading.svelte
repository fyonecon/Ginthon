<script>
    import {loading_data} from "../stores/loading.store.svelte.js"
</script>

<div class="alert_loading-div select-none not-click {loading_data.loading_show}">
    <div class="select-none">
        <div class="loading-info border-radius font-text">
            <div class="alert_loading_msg break select-text">{loading_data.loading_msg}</div>
            <svg class="loading-icon" xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8A8 8 0 0 1 12 20Z" opacity="0.5"/><path fill="currentColor" d="M20 12h2A10 10 0 0 0 12 2V4A8 8 0 0 1 20 12Z"><animateTransform attributeName="transform" dur="1s" from="0 12 12" repeatCount="indefinite" to="360 12 12" type="rotate"/></path></svg>
        </div>
    </div>
</div>

<style>
    .alert_loading-div{
        position: fixed;
        z-index: 100;
        width: 100%;
        height: calc(100% - 50px);
        top: 50px;
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
        max-height: 88px;
        overflow: hidden;
        margin-bottom: 10px;
    }
    .loading-icon{
        width: 50px;
        height: 50px;
        display: block;
        margin: auto auto;
    }

</style>