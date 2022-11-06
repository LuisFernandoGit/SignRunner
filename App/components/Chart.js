import React, { Component, useState } from 'react';
import { Text, View, FlatList, StyleSheet, Platform } from 'react-native';
import { Card, FAB, Button } from 'react-native-paper'
import {Picker} from '@react-native-picker/picker'
import DateTimePicker from '@react-native-community/datetimepicker';
import { VictoryBar, VictoryChart, VictoryTheme } from 'victory-native';

export default function Chart({
  prevW = [100, 200, 300, 150, 150, 350, 500],
  data = [
    {day: 'Dom', score: prevW[0]},
    {day: 'Lun', score: prevW[1]},
    {day: 'Mar', score: prevW[2]},
    {day: 'Mie', score: prevW[3]},
    {day: 'Jue', score: prevW[4]},
    {day: 'Vie', score: prevW[5]},
    {day: 'Sab', score: prevW[6]},
  ]
}) {
  const [chartData, setData] = useState(data);
  const addData = () => {
    var d = [...chartData];
    var obj = {day: "2015", score: 18000};
    d.push(obj);
    setData(d);
  }

  const reset = () =>{
    setData(data);
  }

return (
  <View>
    <VictoryChart width={350} theme={VictoryTheme.material}>
      <VictoryBar animate={{durarion: 3000, onLoad: {duration: 2000}}} data={data} x="day" y="score" />
    </VictoryChart>
  </View>
  );
}
