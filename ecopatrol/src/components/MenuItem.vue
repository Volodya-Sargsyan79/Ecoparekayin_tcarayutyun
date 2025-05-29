<template>
    <div class="menu-item" :class="{ expanded: expanded }">

        <div 
            class="label"
            @click="handleClick"
            :style="{ paddingLeft: depth * 20 + 20 + 'px' }"
        >
            <div class="left">
                <span>{{ label }}</span>
            </div>
            <div v-if="data && data.length" class="right">
                <i class="material-icons expand" :class="{ expanded: expanded }">expand_more</i>
            </div>
        </div>

        <div
            v-show="showChildren"
            class="items-container"
            ref="container"
            :style="{ height: containerHeight }"
        >
            <menu-item 
                v-for="(item, index) in data"
                :key="index"
                :func="item.func"
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
                 expanded: false,
                 containerHeight: 0
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
            },
            func: {
                type: Function
            }
        },
        methods: {
            handleClick() {
                if (this.data && this.data.length > 0) {
                    this.toggleMenu();
                } else if (typeof this.func === 'function') {
                    this.func();
                }
            },
            toggleMenu() {
                this.expanded = !this.expanded
                // If the menu item is closed
                if(!this.showChildren) {
                    this.showChildren = true;
                    this.$nextTick(() => {
                        // We get the height of what's inside thw container to start the animation
                        this.containerHeight = this.$refs["container"].scrollHeight + "px";
                        setTimeout(() => {
                            this.containerHeight = "fit-content"
                            // We set the overflow of the container to visible at the end of the animation
                            this.$refs["container"].style.overflow = "visible";
                        }, 300) // Duration of the animation
                    })
                } else {
                    this.containerHeight = this.$refs["container"].scrollHeight + "px";
                    // we set the overflow of the container to hidden to avoid text overlapping during tre animation
                    this.$refs["container"].style.overflow = "hidden";
                    // This trick allow us to play the animation when the CSS is all well set
                    setTimeout(() => {
                        this.containerHeight = 0 + "px";
                    }, 10)
                    setTimeout(() => {
                        this.showChildren = false;
                    }, 300) // Duration of the animation
                }
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
                font-size: 16px;
                color: #6a6a6a;
                transition: all .3s ease;
                &.expanded {
                    font-size: 16px;
                    color: #6a6a6a;
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
        .items-container {
            width: 100%;
            overflow: hidden;
            transition: height .3s ease;
        }
    }
</style>