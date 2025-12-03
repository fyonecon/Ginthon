<script>
    import { resolve } from '$app/paths';
    import { page } from '$app/state';

</script>

<section class="section-left scroll-y-style">
    <div class="left-logo select-none pywebview-drag-region"></div>
    <div class="left-search font-text">
        <input class="left-search-input" value="" placeholder="..." />
    </div>
    <ul class="left-menu scroll-y-style select-none font-title">
        <li aria-current={page.url.pathname === '/home' ? 'page' : undefined}>
            <a href={resolve('./home')}>Home</a>
        </li>
        <li aria-current={page.url.pathname === '/settings' ? 'page' : undefined}>
            <a href={resolve('./settings')}>Settings</a>
        </li>
        <li class="">
            <a href={resolve('./settings/about')}>About</a>
        </li>
    </ul>
</section>

<style>
    .left-logo{
        height: 50px;
        width: calc(100% - 20px);
        padding: 0 10px;
    }
    .left-search{
        height: 50px;
        width: calc(100% - 20px);
        padding: 0 10px;
    }
    .left-search-input{
        height: 30px;
        width: calc(100% - 20px - 4px);
        padding: 0 10px;
    }
    .left-menu{
        width: calc(100% - 20px);
        padding: 0 10px;
    }
</style>