if (sim_call_type==sim_childscriptcall_initialization) then 
    waveSize=simGetScriptSimulationParameter(sim_handle_self,'waveSize')
    waveVelocity=simGetScriptSimulationParameter(sim_handle_self,'waveVelocity')
    waveAmplitude=simGetScriptSimulationParameter(sim_handle_self,'waveAmplitude')
    wh={-1,-1,-1}
    savedScalingU={1,1,1}
    savedScalingV={1,1,1}
    s=simGetObjectSizeFactor(simGetObjectAssociatedWithScript(sim_handle_self))
    for i=1,3,1 do
        wh[i]=simGetObjectHandle('waterTexture'..i)
        r,savedScalingU[i]=simGetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_scaling_x)
        r,savedScalingV[i]=simGetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_scaling_y)
    end
    pA1={0.33*waveAmplitude,0.4*waveAmplitude,0.45*waveAmplitude}
    pA2={0.27*waveAmplitude,0.3*waveAmplitude,0.34*waveAmplitude}
    pu={0.24*waveVelocity,-0.17*waveVelocity,-0.13*waveVelocity}
    pv={0.37*waveVelocity,0.43*waveVelocity,-0.19*waveVelocity}
end 

if (sim_call_type==sim_childscriptcall_cleanup) then 
    for i=1,3,1 do
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_x,0)
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_y,0)
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_scaling_x,savedScalingU[i])
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_scaling_y,savedScalingV[i])
    end
end 

if (sim_call_type==sim_childscriptcall_sensing) then 
    -- This animates the water (3 layers)
    dt=simGetSimulationTime()
    for i=1,3,1 do
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_x,pA1[i]*math.sin(pu[i]*dt)*s)
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_y,pA2[i]*math.sin(pv[i]*dt)*s)
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_scaling_x,savedScalingU[i]*waveSize/s)
        simSetObjectFloatParameter(wh[i],sim_shapefloatparam_texture_scaling_y,savedScalingV[i]*waveSize/s)
    end
end 
