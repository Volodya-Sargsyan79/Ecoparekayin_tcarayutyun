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
                                children: [
                                    {
                                        label: "Անձնակազմ",
                                        title: "Ա",
                                        func: () => this.employeeKeeper(1)
                                    },
                                    {
                                        label: "Երթուղի",
                                        title: "Ե",
                                        func: () => this.routeKeeper(1)
                                    },
                                    {
                                        label: "Հերթափոխ",
                                        title: "Հ",
                                        func: () => this.placeKeeper(1)
                                    },
                                    
                                ]
                            },
                            {
                                label: 'Գորիսի տեղամաս',
                                children: [
                                    {
                                        label: "Անձնակազմ",
                                        title: "Ա",
                                        func: () => this.employeeKeeper(2)
                                    },
                                    {
                                        label: "Երթուղի",
                                        title: "Ե",
                                        func: () => this.routeKeeper(2)
                                    },
                                    {
                                        label: "Հերթափոխ",
                                        title: "Հ",
                                        func: () => this.placeKeeper(2)
                                    },
                                    
                                ]
                            },
                            {
                                label: 'Սիսիանի տեղամաս',
                                children: [
                                    {
                                        label: "Անձնակազմ",
                                        title: "Ա",
                                        func: () => this.employeeKeeper(3)
                                    },
                                    {
                                        label: "Երթուղի",
                                        title: "Ե",
                                        func: () => this.routeKeeper(3)
                                    },
                                    {
                                        label: "Հերթափոխ",
                                        title: "Հ",
                                        func: () => this.placeKeeper(3)
                                    },
                                    
                                ]
                            },
                            {
                                label: 'Մեղրու տեղամաս',
                                children: [
                                    {
                                        label: "Անձնակազմ",
                                        title: "Ա",
                                        func: () => this.employeeKeeper(4)
                                    },
                                    {
                                        label: "Երթուղի",
                                        title: "Ե",
                                        func: () => this.routeKeeper(4)
                                    },
                                    {
                                        label: "Հերթափոխ",
                                        title: "Հ",
                                        func: () => this.placeKeeper(4)
                                    },
                                    
                                ]
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Կոտայք և Գեղարքունիք',
                        children: [
                            {
                                label: 'Սևանի տեղամաս',
                                title: "Կ",
                                func: () => this.personEmployee()
                            },
                            {
                                label: 'Հրազդանի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Ճամբարակի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Տավուշ',
                        children: [
                            {
                                label: 'Սևքարի տեղամաս',
                                title: "Կ",
                                func: () => this.personEmployee()
                            },
                            {
                                label: 'Նոյեմբերյանի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Դիլիջանի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Իջևանի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Բերդի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Լոռի',
                        children: [
                            {
                                label: 'Ստեփանավանի և Տաշիր տեղամաս',
                                title: "Կ",
                                func: () => this.personEmployee()
                            },
                            {
                                label: 'Վայոցձորի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Թումանյանի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Ախթալայի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Ալավերդու տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Վայոց ձոր և Արարատ',
                        children: [
                            {
                                label: 'Վեդու տեղամաս',
                                title: "Կ",
                                func: () => this.personEmployee()
                            },
                            {
                                label: 'Ջերմուկի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Շիրակ և Արագածոտն',
                        children: [
                            {
                                label: 'Գյումրու տեղամաս',
                                title: "Կ",
                                func: () => this.personEmployee()
                            },
                            {
                                label: 'Ապարանի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            },
                            {
                                label: 'Աշոցքի տեղամաս',
                                title: "Ք",
                                func: () => this.personRelatives()
                            }
                        ]
                    },
                    {
                        label: 'Երևան և ՀՀ Արմավիր',
                        children: [
                            {
                                label: 'Երևանի տեղամաս',
                                title: "Կ",
                                func: () => this.personEmployee()
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
            employeeKeeper(e){
                axios
                    .get("/api/ekopatrol/getlastemployee/", {
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
                    .get('/api/ekopatrol/getlastroute/', {
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