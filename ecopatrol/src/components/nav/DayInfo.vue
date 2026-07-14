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
                        children: [
                            {
                                label: 'Կապանի տեղամաս',
                                children: this.createActions(1)
                            },
                            {
                                label: 'Գորիսի տեղամաս',
                                children: this.createActions(2)
                            },
                            {
                                label: 'Սիսիանի տեղամաս',
                                children: this.createActions(3)
                            },
                            {
                                label: 'Մեղրու տեղամաս',
                                children: this.createActions(4)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Կոտայք և Գեղարքունիք',
                        children: [
                            {
                                label: 'Սևանի տեղամաս',
                                children: this.createActions(5)
                            },
                            {
                                label: 'Հրազդանի տեղամաս',
                                children: this.createActions(6)
                            },
                            {
                                label: 'Ճամբարակի տեղամաս',
                                children: this.createActions(7)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Տավուշ',
                        children: [
                            {
                                label: 'Սևքարի տեղամաս',
                                children: this.createActions(15)
                            },
                            {
                                label: 'Նոյեմբերյանի տեղամաս',
                                children: this.createActions(16)
                            },
                            {
                                label: 'Դիլիջանի տեղամաս',
                                children: this.createActions(17)
                            },
                            {
                                label: 'Իջևանի տեղամաս',
                                children: this.createActions(18)
                            },
                            {
                                label: 'Բերդի տեղամաս',
                                children: this.createActions(19)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Լոռի',
                        children: [
                            {
                                label: 'Ստեփանավանի և Տաշիր տեղամաս',
                                children: this.createActions(8)
                            },
                            {
                                label: 'Վայոցձորի տեղամաս',
                                children: this.createActions(9)
                            },
                            {
                                label: 'Թումանյանի տեղամաս',
                                children: this.createActions(10)
                            },
                            {
                                label: 'Ախթալայի տեղամաս',
                                tchildren: this.createActions(11)
                            },
                            {
                                label: 'Ալավերդու տեղամաս',
                                children: this.createActions(12)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Վայոց ձոր և Արարատ',
                        children: [
                            {
                                label: 'Վեդու տեղամաս',
                                children: this.createActions(13)
                            },
                            {
                                label: 'Ջերմուկի տեղամաս',
                                children: this.createActions(14)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Շիրակ և Արագածոտն',
                        children: [
                            {
                                label: 'Գյումրու տեղամաս',
                                children: this.createActions(20)
                            },
                            {
                                label: 'Ապարանի տեղամաս',
                                children: this.createActions(21)
                            },
                            {
                                label: 'Աշոցքի տեղամաս',
                                children: this.createActions(22)
                            }           
                        ]
                    },
                    {
                        label: 'Երևան և ՀՀ Արմավիր',
                        children: [
                            {
                                label: 'Երևանի տեղամաս',
                                children: this.createActions(23)
                            }
                        ]
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
            createActions(id) {
                return [
                    {
                        label: "Անձնակազմ",
                        title: "Ա",
                        func: () => this.employeeKeeper(id)
                    },
                    {
                        label: "Երթուղի",
                        title: "Ե",
                        func: () => this.routeKeeper(id)
                    },
                    {
                        label: "Հերթափոխ",
                        title: "Հ",
                        func: () => this.placeKeeper(id)
                    }
                ];
            },
            employeeKeeper(e){
                axios
                    .get("/api/ecopatrol/getlastemployee/", {
                        params: { id: e},
                    })
                    .then(res => {
                            this.$store.state.user.employee = res.data
                            this.$router.push('/dashboard/precinct_shift/information/employeelist')
                    })
                    .catch(err => { console.error(err) })
            },
            routeKeeper(e){
                axios
                    .get('/api/ecopatrol/getlastroute/', {
                        params: { id: e},
                    })
                    .then((res) => {
                        this.$store.state.user.route = res.data;
                        this.$router.push('/dashboard/precinct_shift/information/routelist')
                    })
                    .catch(err => console.error(err))
            },
            placeKeeper(e){
                axios
                .get('/api/ecopatrol/getstationshiftlist/', {
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