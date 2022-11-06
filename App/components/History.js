import React, { Component} from 'react';
import { Text, View, StyleSheet, Platform, TouchableOpacity, ScrollView } from 'react-native';
import { Card } from 'react-native-paper'
import { Picker } from '@react-native-picker/picker'
import DateTimePicker from '@react-native-community/datetimepicker';
import { VictoryBar, VictoryChart, VictoryLegend, VictoryLine, VictoryTheme, VictoryAxis } from 'victory-native';
import Icon from 'react-native-vector-icons/FontAwesome';

export default class History extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        week: [],
        prevWeek: 0,
        day: '28',
        month: '7',
        year: '2022',
        difficulty: 'n',
        id: props.route.params.id,
        date: new Date(),
        show: false,
        showC: false,
        prevData: [],
        currentData: []
      };
    }

    async getScores(){
        try{
            this.setState({showC: false})
            console.log(this.state.day);
            console.log(this.state.month);
            console.log(this.state.year);
            const response = await fetch('http://192.168.100.4:5050/historial/'+this.state.difficulty+'/'+this.state.id, {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'content-type':'application/json'
                },
                body: JSON.stringify({
                    day:this.state.day,
                    month:this.state.month,
                    year:this.state.year
                })
            });
            const article = await response.json();
            this.setState({week: article.week});
            this.setState({prevWeek: article.prev_week});
            console.log(this.state.week);
            console.log(this.state.prevWeek);
            await this.setData();
        } catch (error) {
            console.error(error);
        }
    };

    async setData(){
        this.setState({currentData: [
            {day: 'Dom', score: this.state.week[0], label: this.state.week[0]},
            {day: 'Lun', score: this.state.week[1], label: this.state.week[1]},
            {day: 'Mar', score: this.state.week[2], label: this.state.week[2]},
            {day: 'Mie', score: this.state.week[3], label: this.state.week[3]},
            {day: 'Jue', score: this.state.week[4], label: this.state.week[4]},
            {day: 'Vie', score: this.state.week[5], label: this.state.week[5]},
            {day: 'Sab', score: this.state.week[6], label: this.state.week[6]},
        ]});
        this.setState({prevData: [
            {day: 'Dom', score: this.state.prevWeek},
            {day: 'Lun', score: this.state.prevWeek},
            {day: 'Mar', score: this.state.prevWeek},
            {day: 'Mie', score: this.state.prevWeek},
            {day: 'Jue', score: this.state.prevWeek},
            {day: 'Vie', score: this.state.prevWeek},
            {day: 'Sab', score: this.state.prevWeek},
        ]});
        this.setState({showC: true})
        //console.log(this.state.data)
    }

    async setDate(){
        const currentDate = this.state.date;
        this.setState({date: currentDate});

        let tempDate = new Date(currentDate);
        await this.setState({day: tempDate.getDate().toString()});
        await this.setState({month: (tempDate.getMonth()+1).toString()});
        await this.setState({year: tempDate.getFullYear().toString()});
        await this.getScores();
        //await this.setData();
    }
  
    componentDidMount() {
        this.setDate();
        //this.getScores();
    }
  
    render() {
        const renderData = (item) => {
            return(
                <Card style = {styles.cardStyle}>
                    <Text style = {{fontSize: 16}}>{item}</Text>
                </Card>
            )
        }

        const Ver = () =>{
            this.setState({visible: !this.state.visible})
        };

        const onChange = (event, selectedDate) =>{
            const currentDate = selectedDate || this.state.date;
            if (Platform.OS === 'android') {
                this.setState({show: false})
            }
            this.setState({date: currentDate});

            let tempDate = new Date(currentDate);
            this.setState({day: tempDate.getDate().toString()});
            this.setState({month: (tempDate.getMonth()+1).toString()});
            this.setState({year: tempDate.getFullYear().toString()});
        }

        const emptyData = [
            {day: 'Dom', score: 0},
            {day: 'Lun', score: 0},
            {day: 'Mar', score: 0},
            {day: 'Mie', score: 0},
            {day: 'Jue', score: 0},
            {day: 'Vie', score: 0},
            {day: 'Sab', score: 0},
          ]
      
        return (
            <View style = {{flex: 1}}>
                <View>
                    <Text style={{fontSize: 18, marginLeft: 18, marginTop: 15, color: '#f0ffff', fontWeight: 'bold'}}>Dificultad</Text>
                    <View style={{borderColor: '#b0e0e6', borderBottomWidth: 1, width: 120, marginLeft: 18, marginBottom: 20}}>
                        <Picker
                        onValueChange={(difficulty)=>this.setState({difficulty})}
                        selectedValue = {this.state.difficulty}
                        style={styles.picker}
                        >
                            <Picker.Item label = "Fácil" value = "e" style={{fontSize:16}}/>
                            <Picker.Item label = "Normal" value = "n" style={{fontSize:16}}/>
                            <Picker.Item label = "Difícil" value = "h" style={{fontSize:16}}/>
                        </Picker>
                    </View>

                    <View style={{marginTop: -95, marginLeft: 165}}>
                        <Text style={{fontSize: 18, marginLeft: 18, color: '#f0ffff', fontWeight: 'bold'}}>Fecha</Text>
                        <View style={styles.fecha}>
                            <TouchableOpacity onPress = {() => this.setState({show: true})}>
                                <Icon name="calendar" size={20} style={{height: 20, textAlignVertical: 'center', color: '#f0fff0'}}>
                                    <Text style={{fontSize:16}}>  {this.state.day+"/"+this.state.month+"/"+this.state.year}</Text>
                                </Icon>
                                <Icon name="sort-down" size={15} style={{marginLeft: 137, marginTop: -22}}></Icon>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
                
                <View>
                    <VictoryLegend 
                    x = {40}
                    y = {30}
                    style={styles.chartLabels}
                    data={[
                    {
                        name: "Mejores puntajes de la semana",
                        symbol: {
                            fill: "#3cb371",
                            stroke: "#2e8b57",
                            strokeWidth: 2,
                        },
                    },
                    {
                        name: "Mejor puntaje de la semana anterior",
                        symbol: {
                            fill: "#dc143c",
                            stroke: "#8b0000",
                            strokeWidth: 2,
                        },
                    }
                ]}></VictoryLegend>
                </View>

                {this.state.showC && (
                    <View marginLeft={10} marginTop={-220}>
                        <VictoryChart width={360} height={320} style={styles.chart} theme={VictoryTheme.material}>
                            <VictoryAxis
                            style={{
                            tickLabels: { fontSize: 14, fill: "#f0fff0" }
                            }}
                            />
                            <VictoryAxis dependentAxis
                            style={{
                            tickLabels: { fontSize: 14, fill: "#f0fff0" }
                            }}/>

                            <VictoryBar style={styles.bars}
                            domainPadding={{x: 30, y: 0 }} 
                            animate={{durarion: 2000, onLoad: {duration: 2000}}} 
                            data={this.state.currentData} x="day" y="score" />
                            <VictoryLine style={{
                                data: {
                                    stroke: "#dc143c",
                                    strokeWidth: 5,
                                },
                            }}
                            domainPadding={{x: -30, y: 0 }} 
                            data={this.state.prevData} x="day" y="score" />
                        </VictoryChart>
                    </View>
                )}

                {!this.state.showC && (
                    <View marginLeft={10} marginTop={-220}>
                        <VictoryChart width={360} height={320} style={styles.chart} theme={VictoryTheme.material} domain={{y: [0, 10] }}>
                            <VictoryAxis
                            style={{
                            tickLabels: { fontSize: 14, fill: "#f0fff0" }
                            }}
                            />
                            <VictoryAxis dependentAxis
                            tickValues={[2, 4, 6, 8, 10]}
                            style={{
                            tickLabels: { fontSize: 14, fill: "#f0fff0" }
                            }}/>
                            <VictoryBar domainPadding={{x: 30, y: 0 }} data={emptyData} x="day" y="score"/>
                            <VictoryLine style={{
                                data: {
                                    stroke: "#dc143c",
                                    strokeWidth: 5,
                                },
                            }}
                            domainPadding={{x: -30, y: 0 }} 
                            data={emptyData} x="day" y="score" />
                        </VictoryChart>
                    </View>
                )}

                <View style={styles.boton} >
                    <TouchableOpacity onPress={() => this.getScores()}>
                        <Icon name="refresh" size={16} color="#f0ffff" style={{height: 20, textAlignVertical: 'center'}}>
                            <Text style={{fontSize: 16}}>  Actualizar Puntajes</Text>
                        </Icon>
                    </TouchableOpacity>
                </View>

                {this.state.show && (
                    <DateTimePicker
                    testID='dateTimePicker'
                    value={this.state.date}
                    mode={'date'}
                    is24Hour={true}
                    display='default'
                    onChange={onChange}
                    />
                )}
            </View>
        );
    }
};

const styles = StyleSheet.create({
    cardStyle: {
        margin: 18,
        padding: 10,
        marginBottom: -5
    },
    fab: {
        position: 'absolute',
        margin: 16,
        right: 0,
        bottom: 0
    },
    spliters: {
        margin: 18,
        marginBottom: -5,
        borderBottomWidth: 2,
        borderBottomColor: '#f0ffff'
    },
    fecha: {
        marginLeft: 18, 
        marginTop: 18, 
        borderBottomWidth: 1,
        height: 32,
        width: 157,
        borderBottomColor: '#b0e0e6'
    },
    picker: {
        height: 50,
        width: 140,
        marginLeft: -10,
        color: '#f0fff0'
    },
    boton: {
        borderWidth: 3, 
        borderRadius: 6,
        borderColor: '#00ced1',
        marginLeft: 80, 
        marginTop: 15, 
        marginBottom: 15, 
        width: 200,
        alignItems: 'center',
        backgroundColor: '#008b8b',
        padding: 10,
    },
    chartLabels: {
        labels: {fill: '#f0fff0',
        fontFamily: "inherit",
        fontSize: 15,
        fontStyle: "italic"}
    },
    bars: {
        data: {
            fill: "#3cb371",
            width: 20,
            stroke: "#2e8b57",
            strokeWidth: 1,
        },
        labels: { fill: "#f0f8ff", fontSize: 12, fontWeight: 'bold' }
    },
    chart: {
        background: {fill: "#008b8b", fillOpacity: 0.3}
      }
});