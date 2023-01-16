            <Ceiling id="4">
                <Label>Ceiling01</Label>
                <Construction>
                    <Type code="2">
                        <English>Attic/gable</English>
                        <French>Combles/pignon</French>
                    </Type>
                    <CeilingType idref="Code 2" rValue="6.0448" nominalInsulation="6.2521">2401551000</CeilingType>
                </Construction>
                <Measurements length="23.672" area="104.0148" heelHeight="0.13">
                    <Slope code="0" value="0.3333">
                        <English>User specified</English>
                        <French>Spécifié par l'utilisateur</French>
                    </Slope>
                </Measurements>
            </Ceiling>
            <Wall adjacentEnclosedSpace="false" id="2">
                <Label>Main floor</Label>
                <Construction corners="4" intersections="4">
                    <Type idref="Code 1" rValue="2.9921" nominalInsulation="3.2421">1211301121</Type>
                    <LintelType idref="Code 5">101</LintelType>
                </Construction>
                <Measurements height="2.4384" perimeter="41.2486" />
                <FacingDirection code="_FRONT_">
                    <English>N/A</English>
                    <French>S/O</French>
                </FacingDirection>
                <Components>
#include "doors.i"
#include "windows.i"
                </Components>
            </Wall>
            <Floor adjacentEnclosedSpace="true" id="42">
                <Label>Floor - 1</Label>
                <Construction>
                    <Type idref="Code 3" rValue="5.7218" nominalInsulation="5.3242">3231L06B00</Type>
                </Construction>
                <Measurements area="0.0929" length="0.3048" />
            </Floor>
            <Basement isExposedSurface="true" exposedSurfacePerimeter="39.624" id="1">
                <Label>Foundation - 1</Label>
                <Configuration type="BCCB" subtype="8" overlap="0.0914">BCCB_8</Configuration>
                <OpeningUpstairs code="4" value="1.5598">
                    <English>User specified</English>
                    <French>Spécifié par l'utilisateur</French>
                </OpeningUpstairs>
                <RoomType code="6">
                    <English>Utility Room</English>
                    <French>Pièce Utilitaire</French>
                </RoomType>
                <Floor>
                    <Construction isBelowFrostline="true" hasIntegralFooting="false" heatedFloor="false">
                        <AddedToSlab rValue="0.0018" nominalInsulation="0.0018">User specified</AddedToSlab>
                        <FloorsAbove idref="Code 7" rValue="0.9834" nominalInsulation="0">4231002760</FloorsAbove>
                    </Construction>
                    <Measurements isRectangular="false" area="92.903" perimeter="39.624" />
                </Floor>
                <Wall hasPonyWall="true">
                    <Construction corners="4">
                        <InteriorAddedInsulation idref="Code 8" nominalInsulation="2.11">
                            <Description>230201</Description>
                            <Composite>
                                <Section rank="1" percentage="100" rsi="1.7329" nominalRsi="2.11" />
                            </Composite>
                        </InteriorAddedInsulation>
                        <ExteriorAddedInsulation nominalInsulation="0.0018">
                            <Description>User specified</Description>
                            <Composite>
                                <Section rank="1" percentage="100" rsi="0.0018" nominalRsi="0.0018" />
                            </Composite>
                        </ExteriorAddedInsulation>
                        <Lintels idref="Code 4">Bsmnt Lintel</Lintels>
                        <PonyWallType idref="Code 9" nominalInsulation="3.2421">
                            <Description>1211301121</Description>
                            <Composite>
                                <Section rank="1" percentage="100" rsi="2.8703" nominalRsi="3.2421" />
                            </Composite>
                        </PonyWallType>
                    </Construction>
                    <Measurements height="2.3622" depth="0.9144" ponyWallHeight="1.2192" />
                </Wall>
                <Components>
                    <FloorHeader adjacentEnclosedSpace="false" id="3">
                        <Label>BW hdr-01</Label>
                        <Construction>
                            <Type idref="Code 10" rValue="3.6896" nominalInsulation="3.34">R-19 + siding</Type>
                        </Construction>
                        <Measurements height="0.3048" perimeter="40.2336" />
                        <FacingDirection code="1">
                            <English>N/A</English>
                            <French>S/O</French>
                        </FacingDirection>
                    </FloorHeader>
                </Components>
            </Basement>