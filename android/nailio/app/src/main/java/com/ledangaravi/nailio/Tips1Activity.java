package com.ledangaravi.nailio;

import android.content.Intent;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TableLayout;
import android.widget.TextView;

public class Tips1Activity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_tips1);

        TextView textViewCustom = findViewById(R.id.tips1_custom);
        //TextView textViewGeneral = findViewById(R.id.tips1_general);
        TableLayout tableLayout = findViewById(R.id.table);



        switch(EvalActivity.diagnosis) {
            case "Normal":
                textViewCustom.setText(R.string.verdict_normal);
                tableLayout.setVisibility(View.VISIBLE);
                //textViewGeneral.setVisibility(View.VISIBLE);
                break;
            case "Other":
                textViewCustom.setText(R.string.verdict_other);
                tableLayout.setVisibility(View.VISIBLE);
                //textViewGeneral.setVisibility(View.VISIBLE);
                break;
            case "Nail dystrophy":
                textViewCustom.setText(R.string.verdict_naildystrophy);
                tableLayout.setVisibility(View.VISIBLE);
                //textViewGeneral.setVisibility(View.VISIBLE);
                break;
            case "Onychomycosis":
                textViewCustom.setText(R.string.verdict_onychomycosis);
                break;
            case "Onycholysis":
                textViewCustom.setText(R.string.verdict_onycholysis);
                break;
            case "Melanonychia":
                textViewCustom.setText(R.string.verdict_melanonychia);
                break;
            default:
                // code block
        }

        FloatingActionButton fabHome = (FloatingActionButton) findViewById(R.id.tips_fab_home);
        fabHome.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                startActivity(intent);
            }
        });
    }
}
