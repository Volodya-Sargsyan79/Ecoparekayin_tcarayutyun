<template>
    <div class="menu">
        <MenuItem 
            v-for="(item, index) in menuTree"
            :key="index"
            :label="item.label"
            :depth="0"
            :data="item.children"
        />
    </div>
</template>

<script>
    import MenuItem from './MenuItem.vue';
    export default {
        name: 'recursive-menu',
        data() {
            return {
                menuTree: [
                    {
                        label: 'Home',
                        children: [
                            {
                                label: 'level 1.1',
                            },
                            {
                                label: 'level 1.2',
                            },
                        ]
                    },
                    {
                        label: "Settings",
                    }
                    
                ]
            }
            
        },
        components: {
            MenuItem
        }
    }
</script>

<style lang="scss" scoped>
    .menu {
        height: 100vh;
        width: 240px;
        transition: all .3s ease;
        overflow: auto;
    }
</style>