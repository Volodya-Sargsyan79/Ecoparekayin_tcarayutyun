<template>
    <div class="menu-item" :class="{ expanded: expanded }">
        <div 
            class="label"
            @click="toggleMenu()"
        >
            <div class="left">
                <span>{{ label }}</span>
            </div>
            <div v-if="data" class="right">
                <i class="material-icons expand" :class="{ expanded: expanded }">expand_more</i>
            </div>
        </div>
        
        <div 
            v-show="showChildren"
            class="items-container"
        >
            <menu-item 
                v-for="(item, index) in data"
                :key="index"
                :label="item.label"
                :depth="depth + 1"
                :data="item.children"
            />
        </div>
    </div>
</template>

<script>
    export default {
        name: 'menu-item',
        data() {
            return{
                 showChildren: false,
                 expanded: false
            }
        },
        props: {
            label: {
                type: String,
                required: true
            },
            depth: {
                type: Number,
                required: true
            },
            data: {
                type: Array
            }
        },
        methods: {
            toggleMenu() {
                this.expanded = !this.expanded
                this.showChildren = !this.showChildren
            }
        }
    }
    
</script>

<style lang="scss" scoped>
    .menu-item {
        width: 100%;
        .label {
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            white-space: nowrap;
            user-select: none;
            height: 50px;
            padding: 0 20px;
            box-sizing: border-box;
            color: #6a6a6a;
            transition: all .3s ease;
            > div {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            i {
                font-size: 20pz;
                color: #6a6a6a;
                transition: all .3s ease;
                &.expanded {
                    font-size: 16px;
                    color: #cacaca;
                    &.expanded {
                        transform: rotate(180deg);
                    }
                }
            }
            &:hover {
                background-color: #deedff;
                cursor: pointer;
            }
        }
    }
</style>