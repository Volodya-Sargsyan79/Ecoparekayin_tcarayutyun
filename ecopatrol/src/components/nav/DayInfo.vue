<template>
    <div class="menu">
        <MenuItem 
            v-for="(item, index) in visibleMenuTree"
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
        name: 'DayInfo',
        data() {
            return {
                menuTree: [
                    {
                        label: 'ՀՀ Սյունիքի',
                        regionId: 1,
                        children: [
                            {
                                label: 'Կապանի տեղամաս',
                                precinctId: 1,
                                children: this.createActions(1)
                            },
                            {
                                label: 'Գորիսի տեղամաս',
                                precinctId: 2,
                                children: this.createActions(2)
                            },
                            {
                                label: 'Սիսիանի տեղամաս',
                                precinctId: 3,
                                children: this.createActions(3)
                            },
                            {
                                label: 'Մեղրու տեղամաս',
                                precinctId: 4,
                                children: this.createActions(4)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Կոտայք և Գեղարքունիք',
                        regionId: 2,
                        children: [
                            {
                                label: 'Սևանի տեղամաս',
                                precinctId: 5,
                                children: this.createActions(5)
                            },
                            {
                                label: 'Հրազդանի տեղամաս',
                                precinctId: 6,
                                children: this.createActions(6)
                            },
                            {
                                label: 'Ճամբարակի տեղամաս',
                                precinctId: 7,
                                children: this.createActions(7)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Տավուշ',
                        regionId: 3,
                        children: [
                            {
                                label: 'Սևքարի տեղամաս',
                                precinctId: 15,
                                children: this.createActions(15)
                            },
                            {
                                label: 'Նոյեմբերյանի տեղամաս',
                                precinctId: 16,
                                children: this.createActions(16)
                            },
                            {
                                label: 'Դիլիջանի տեղամաս',
                                precinctId: 17,
                                children: this.createActions(17)
                            },
                            {
                                label: 'Իջևանի տեղամաս',
                                precinctId: 18,
                                children: this.createActions(18)
                            },
                            {
                                label: 'Բերդի տեղամաս',
                                precinctId: 19,
                                children: this.createActions(19)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Լոռի',
                        regionId: 4,
                        children: [
                            {
                                label: 'Ստեփանավանի և Տաշիր տեղամաս',
                                precinctId: 8,
                                children: this.createActions(8)
                            },
                            {
                                label: 'Վայոցձորի տեղամաս',
                                precinctId: 9,
                                children: this.createActions(9)
                            },
                            {
                                label: 'Թումանյանի տեղամաս',
                                precinctId: 10,
                                children: this.createActions(10)
                            },
                            {
                                label: 'Ախթալայի տեղամաս',
                                precinctId: 11,
                                children: this.createActions(11)
                            },
                            {
                                label: 'Ալավերդու տեղամաս',
                                precinctId: 12,
                                children: this.createActions(12)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Վայոց ձոր և Արարատ',
                        regionId: 5,
                        children: [
                            {
                                label: 'Վեդու տեղամաս',
                                precinctId: 13, 
                                children: this.createActions(13)
                            },
                            {
                                label: 'Ջերմուկի տեղամաս',
                                precinctId: 14,
                                children: this.createActions(14)
                            }
                        ]
                    },
                    {
                        label: 'ՀՀ Շիրակ և Արագածոտն',
                        regionId: 6,
                        children: [
                            {
                                label: 'Գյումրու տեղամաս',
                                precinctId: 20,
                                children: this.createActions(20)
                            },
                            {
                                label: 'Ապարանի տեղամաս',
                                precinctId: 21,
                                children: this.createActions(21)
                            },
                            {
                                label: 'Աշոցքի տեղամաս',
                                precinctId: 22,
                                children: this.createActions(22)
                            }           
                        ]
                    },
                    {
                        label: 'Երևան և ՀՀ Արմավիր',
                        regionId: 7,
                        children: [
                            {
                                label: 'Երևանի տեղամաս',
                                precinctId: 23,
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
        computed: {
            visibleMenuTree() {
                const user = this.$store.state.user
                const groups = user.groups || []
                if (user.isLoading || !groups.length) {
                    return []
                }
                const isDutyOfficer = groups.includes('Հերթապահներ')
                const isPrecinctHead = groups.includes('Տեղամասի պետեր')
                const isRegionHead = groups.includes('Վարչության պետեր')
                const regionId = Number(user.region_id)
                const precinctId = Number(user.precinct_id)
                if (
                    !isDutyOfficer &&
                    !isPrecinctHead &&
                    !isRegionHead
                ) {
                    return this.menuTree
                }
                if (!regionId) {
                    return []
                }
                if (isRegionHead) {
                    return this.menuTree.filter(
                        region => Number(region.regionId) === regionId
                    )
                }
                if (!precinctId) {
                    return []
                }
                return this.menuTree
                .filter(
                    region => Number(region.regionId) === regionId
                )
                .map(region => ({
                    ...region,

                    children: (region.children || []).filter(
                        precinct =>
                            Number(precinct.precinctId) === precinctId
                    )
                }))
                .filter(region => region.children.length > 0)
            }
        },
        methods: {
            createActions(id) {
                const groups = this.$store.state.user.groups || []
                const isDutyOfficer = groups.includes('Հերթապահներ')
                const actions = [
                    {
                        label: "Անձնակազմ",
                        title: "Ա",
                        func: () => this.employeeKeeper(id)
                    },
                    {
                        label: "Հերթափոխ",
                        title: "Հ",
                        func: () => this.placeKeeper(id)
                    }
                ]
                if (!isDutyOfficer) {
                    actions.splice(1, 0, {
                        label: "Երթուղի",
                        title: "Ե",
                        func: () => this.routeKeeper(id)
                    })
                }
                return actions
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
            async placeKeeper(e) {
                this.$store.state.user.filelist = null
                this.$store.state.user.stationshif = []

                try {
                    const [shiftResponse, fileResponse] = await Promise.all([
                        axios.get('/api/ecopatrol/getstationshiftlist/', {
                            params: { id: e }
                        }),

                        axios.get('/api/ecopatrol/getshiftdayinfo/', {
                            params: { id: e }
                        })
                    ])
                    this.$store.state.user.stationshif = shiftResponse.data
                    this.$store.state.user.filelist = fileResponse.data
                    this.$router.push(
                        '/dashboard/precinct_shift/information/shitlist'
                    )
                } catch (err) {
                    console.error(err)
                    this.$store.state.user.filelist = []
                }
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