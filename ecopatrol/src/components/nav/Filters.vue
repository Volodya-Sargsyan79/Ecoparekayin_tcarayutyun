<template>
    <div class="menu">
        <MenuItem 
            v-for="(item, index) in menuTree"
            :key="index"
            :label="item.label"
            :title="item.title"
            :func="item.func"
            :depth="0"
            :data="item.children"
        />
    </div>
</template>

<script>
    import axios from 'axios';
    import MenuItem from './MenuItem.vue';
    export default {
        name: 'Filters',
        data() {
            return {
                menuTree: [
                    {
                        label: 'ՀՀ Սյունիքի',
                        title: "Ս",
                        func: () => this.searchShifth(1)
                    },
                    {
                        label: 'ՀՀ Կոտայք և Գեղարքունիք',
                        title: "Կ",
                        func: () => this.searchShifth(2)
                    },
                    {
                        label: 'ՀՀ Տավուշ',
                        title: "Տ",
                        func: () => this.searchShifth(3)
                    },
                    {
                        label: 'ՀՀ Լոռի',
                        title: "Լ",
                        func: () => this.searchShifth(4)
                    },
                    {
                        label: 'ՀՀ Վայոց ձոր և Արարատ',
                        title: "Վ",
                        func: () => this.searchShifth(5)
                    },
                    {
                        label: 'ՀՀ Շիրակ և Արագածոտն',
                        title: "Շ",
                        func: () => this.searchShifth(6)
                    },
                    {
                        label: 'Երևան և ՀՀ Արմավիր',
                        title: "Ե",
                        func: () => this.searchShifth(7)
                    }
                ],
                limit: 10,
                offset: 0
            }
            
        },
        components: {
            MenuItem
        },
        methods: {
            searchShifth(e){

                axios
                    .get("/api/ekopatrol/precinct/", {
                        params: { id: e },
                    })
                    .then((res) => {
                        this.$store.state.user.precincts = res.data;
                        this.$router.push('/dashboard/precinct_shift/search_information/searchshift')
                    })
                    .catch((err) => {
                        console.error(err);
                    });
            },
            placeKeeper(e){
                axios
                .get('/api/ekopatrol/getstationshiftlist/', {
                    params: { id: e},
                }) 
                .then((res) => {
                    this.$store.state.user.stationshif = res.data;
                    this.$router.push('/dashboard/precinct_shift/information/shitlist') 
                })
                .catch(err => { console.error(err) }) 

            }
        }
    }
</script>

<style lang="scss" scoped>
    .menu {
        width: 100%;
        transition: all .3s ease;
        overflow: auto;
    }
</style>