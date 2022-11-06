import React, { Component } from 'react';
import { Text, View, FlatList, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { Card, FAB } from 'react-native-paper'
import {Picker} from '@react-native-picker/picker'
import Donut from './Donut';
import Icon from 'react-native-vector-icons/FontAwesome';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default class Home extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        lastScore: 0,
        lastTen: [],
        difficulty: 'n',
        id: props.route.params.id,
        promedio: 0,
        max: 100,
        porcentaje: 0,
        negative: false
      };
    }

    async getScores() {
        try{
            //Replace "0.0.0.0" for your local ip (shown in the api.py console).
            const response = await fetch('http://0.0.0.0:5050/promedio/'+this.state.difficulty+'/'+this.state.id);
            const article = await response.json();
            this.setState({lastScore: article.last});
            this.setState({lastTen: article.last_ten});
            if(article.last != 0){
                this.setState({max: article.last});
            }

            let sum = 0;
            for(let i=0; i<this.state.lastTen.length; i++){
                sum = sum + this.state.lastTen[i];
                if(this.state.max < this.state.lastTen[i]){
                    this.setState({max: this.state.lastTen[i]});
                }
            }
            this.setState({promedio: sum/this.state.lastTen.length});
            
            let porcent = this.state.lastScore - this.state.promedio;
            if(porcent != 0 || this.state.promedio != 0){
                porcent = porcent / this.state.promedio;
                porcent = porcent*100;
            }
            if(porcent < 0){
                this.setState({negative: true});
                porcent = porcent*-1;
            } else {
                this.setState({negative: false});
            }
            this.setState({porcentaje: Math.round(porcent)});

            console.log(this.state.lastScore);
            console.log(this.state.lastTen);
            console.log(this.state.promedio);
            console.log(this.state.max);
            console.log(this.state.porcentaje);

        } catch (error) {
            console.error(error);
        }
    };
  
    componentDidMount() {
        this.getScores();
    }
  
    render() {
        const Salir = () =>{
            AsyncStorage.clear()
            this.props.navigation.navigate("Iniciar Sesión")
        }
      
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
                </View>

                <View style={styles.boton2} >
                    <TouchableOpacity onPress = {() => this.props.navigation.navigate("Puntajes Semanales")}>
                        <Text style={
                            {fontSize: 14, 
                            color: "#f0ffff", 
                            fontStyle: "italic", 
                            marginTop: -5, 
                            marginLeft: 5}}>    Puntajes Semanales</Text>
                    </TouchableOpacity>
                </View>

                {!this.state.negative && (
                    <View style={{marginLeft: 10, marginTop: 20}}>
                        <View>
                            <Donut percentage={this.state.lastScore} color={"#90ee90"} strokeColor={"#2e8b57"} max={this.state.max}/>
                            <Text style={styles.donutText}>pts.</Text>
                        </View>
                        <View style={{marginLeft: 175, marginTop: -35}}>
                            <Donut percentage={this.state.porcentaje} color={"#90ee90"} strokeColor={"#2e8b57"} max={100}/>
                            <Text style={styles.donutText}>%</Text>
                        </View>

                        <View style = {styles.spliters}>
                            <Text style = {{fontSize: 16, color: '#f0ffff'}}>
                                Tu última puntuación <Text style = {{fontSize: 16, color: '#f0ffff', fontWeight: 'bold'}}>{"("+this.state.lastScore+")"} </Text>
                                fue <Text style = {{fontSize: 16, color: '#90ee90', fontWeight: 'bold'}}>{this.state.porcentaje}% mejor </Text>
                                que tu puntuación promedio <Text style = {{fontSize: 16, color: '', fontWeight: 'bold'}}>{"("+this.state.promedio.toFixed(0)+")"}</Text> </Text>
                        </View>
                    </View>
                )}
                {this.state.negative && (
                    <View style={{marginLeft: 10, marginTop: 20}}>
                        <View>
                            <Donut percentage={this.state.lastScore} color={"#dc143c"} strokeColor={"#8b0000"} max={this.state.max}/>
                            <Text style={styles.donutText}>pts.</Text>
                        </View>
                        <View style={{marginLeft: 175, marginTop: -35}}>
                            <Donut percentage={this.state.porcentaje} color={"#dc143c"} strokeColor={"#8b0000"} max={100}/>
                            <Text style={styles.donutText}>%</Text>
                        </View>

                        <View style = {styles.spliters}>
                            <Text style = {{fontSize: 16, color: '#f0ffff'}}>
                                Tu última puntuación <Text style = {{fontSize: 16, color: '#f0ffff', fontWeight: 'bold'}}>{"("+this.state.lastScore+")"} </Text>
                                fue <Text style = {{fontSize: 16, color: '#dc143c', fontWeight: 'bold'}}>{this.state.porcentaje}% peor </Text>
                                que tu puntuación promedio <Text style = {{fontSize: 16, color: '', fontWeight: 'bold'}}>{"("+this.state.promedio.toFixed(2)+")."}</Text> </Text>
                        </View>
                    </View>
                )}

                <View style={styles.boton} >
                    <TouchableOpacity onPress={() => this.getScores()}>
                        <Icon name="refresh" size={16} color="#f0ffff" style={{height: 20, textAlignVertical: 'center'}}>
                            <Text style={{fontSize: 16}}>  Actualizar Puntajes</Text>
                        </Icon>
                    </TouchableOpacity>
                </View>   

                <View style={styles.boton} >
                    <TouchableOpacity onPress={Salir}>
                        <Icon name="sign-out" size={16} color="#f0ffff" style={{height: 20, textAlignVertical: 'center'}}>
                            <Text style={{fontSize: 16}}>  Cerrar Sesión</Text>
                        </Icon>
                    </TouchableOpacity>
                </View> 
                <FAB
                    style = {styles.fab}
                    small = {false}
                    icon = "calendar-month"
                    theme = {{colors: {accent: "green"}}}
                    //onPress={() => console.log("presionado")}
                    onPress = {() => this.props.navigation.navigate("Puntajes Semanales", {id: this.state.id})}
                />           
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
        margin: 10,
        right: 10,
        top: 18,
        borderWidth: 3, 
        borderColor: '#00ced1',
        backgroundColor: '#008b8b'
    },
    spliters: {
        height: 55,
        margin: 18,
        marginTop: 155,
        borderBottomWidth: 2,
        borderBottomColor: '#b0e0e6'
    },
    fecha: {
        marginLeft: 18, 
        marginTop: 18, 
        borderBottomWidth: 1,
        height: 32,
        width: 157
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
        marginTop: 25, 
        marginBottom: 10, 
        width: 200,
        alignItems: 'center',
        backgroundColor: '#008b8b',
        padding: 10,
    },
    donutText: {
        color: '#b0e0e6',
        fontFamily: "inherit",
        fontSize: 18,
        fontStyle: "italic",
        marginLeft: 145, 
        marginTop: -150, 
    },
    boton2: {
        borderRadius: 20,
        marginTop: -75, 
        marginBottom: 25, 
        marginLeft: 183,
        width: 130,
        height: 48,
        backgroundColor: '#008b8b',
        padding: 10,
        justifyContent: "center"
    }
});

//export default Home;
