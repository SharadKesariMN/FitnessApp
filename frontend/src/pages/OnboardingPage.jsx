import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import axios from 'axios';
import { toast } from 'sonner';
import { Activity, User, Weight, Calendar, Ruler } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const OnboardingPage = ({ user }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    height: '',
    weight: '',
    date_of_birth: '',
    age: '',
  });
  const [bmi, setBmi] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    if (name === 'date_of_birth' && value) {
      const birthDate = new Date(value);
      const today = new Date();
      const calculatedAge = today.getFullYear() - birthDate.getFullYear();
      setFormData((prev) => ({ ...prev, age: calculatedAge.toString() }));
    }

    if (name === 'height' || name === 'weight') {
      const h = name === 'height' ? parseFloat(value) : parseFloat(formData.height);
      const w = name === 'weight' ? parseFloat(value) : parseFloat(formData.weight);
      if (h && w) {
        const calculatedBmi = w / ((h / 100) ** 2);
        setBmi(calculatedBmi.toFixed(2));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.height || !formData.weight || !formData.date_of_birth) {
      toast.error('Please fill in all required fields');
      return;
    }

    try {
      await axios.put(
        `${BACKEND_URL}/api/user/onboarding`,
        {
          height: parseFloat(formData.height),
          weight: parseFloat(formData.weight),
          date_of_birth: formData.date_of_birth,
          age: parseInt(formData.age),
          selected_sports: [],
        },
        { withCredentials: true }
      );

      toast.success('Profile updated!');
      navigate('/purpose');
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  return (
    <div className="min-h-screen bg-background py-12 px-4">
      <div className="container max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="text-center mb-8">
            <Activity className="w-12 h-12 text-volt-blue mx-auto mb-4" />
            <h1 className="text-4xl font-heading font-black tracking-tight mb-2">
              Let's Get Started
            </h1>
            <p className="text-muted-foreground">
              Tell us about yourself to personalize your fitness journey
            </p>
          </div>

          <Card data-testid="onboarding-form-card" className="border border-border">
            <CardHeader>
              <CardTitle className="font-heading">Personal Information</CardTitle>
              <CardDescription>We'll calculate your BMI and create a custom plan</CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <Label htmlFor="height" className="flex items-center gap-2">
                      <Ruler className="w-4 h-4 text-volt-blue" />
                      Height (cm) *
                    </Label>
                    <Input
                      data-testid="height-input"
                      id="height"
                      name="height"
                      type="number"
                      placeholder="170"
                      value={formData.height}
                      onChange={handleChange}
                      required
                      className="border-border"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="weight" className="flex items-center gap-2">
                      <Weight className="w-4 h-4 text-volt-blue" />
                      Weight (kg) *
                    </Label>
                    <Input
                      data-testid="weight-input"
                      id="weight"
                      name="weight"
                      type="number"
                      placeholder="70"
                      value={formData.weight}
                      onChange={handleChange}
                      required
                      className="border-border"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="date_of_birth" className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-volt-blue" />
                    Date of Birth *
                  </Label>
                  <Input
                    data-testid="dob-input"
                    id="date_of_birth"
                    name="date_of_birth"
                    type="date"
                    value={formData.date_of_birth}
                    onChange={handleChange}
                    max={new Date().toISOString().split('T')[0]}
                    required
                    className="border-border"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="age" className="flex items-center gap-2">
                    <User className="w-4 h-4 text-volt-blue" />
                    Age
                  </Label>
                  <Input
                    data-testid="age-input"
                    id="age"
                    name="age"
                    type="number"
                    placeholder="Auto-calculated"
                    value={formData.age}
                    readOnly
                    className="border-border bg-muted"
                  />
                </div>

                {bmi && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="p-4 bg-volt-blue/10 border border-volt-blue/30 rounded-lg"
                    data-testid="bmi-display"
                  >
                    <p className="text-sm font-medium text-volt-blue">
                      Your BMI: <span className="text-lg font-bold">{bmi}</span>
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {bmi < 18.5
                        ? 'Underweight'
                        : bmi < 25
                        ? 'Normal weight'
                        : bmi < 30
                        ? 'Overweight'
                        : 'Obese'}
                    </p>
                  </motion.div>
                )}

                <Button
                  data-testid="onboarding-submit-btn"
                  type="submit"
                  className="w-full btn-hover bg-volt-blue hover:bg-volt-blue/90 font-bold py-6 text-lg"
                  size="lg"
                >
                  Continue
                </Button>
              </form>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

export default OnboardingPage;
